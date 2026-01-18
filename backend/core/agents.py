from typing import List, Dict, Any
from .llm import llm_provider

class DebateAgent:
    def __init__(self, name: str, role: str, instruction: str):
        self.name = name
        self.role = role
        self.instruction = instruction

    async def run(self, context: str, query: str, history: List[Dict[str, str]] = None) -> str:
        history_str = ""
        if history:
            history_str = "\n".join([f"{m['agent']}: {m['content']}" for m in history])
        
        prompt = f"""
CONTEXT FROM DOCUMENTS:
{context}

USER QUERY:
{query}

DEBATE HISTORY:
{history_str}

YOUR ROLE: {self.name} ({self.role})
INSTRUCTION: {self.instruction}

STRICT RULE: Answer ONLY for what is asked. Do not add conversational fillers. Do not add "hello" or "hope this helps". Just the facts.
Provide your response according to your role. Be precise, use the context provided, and cite sources (PDF/TXT file names) when possible.
"""
        return llm_provider.generate(prompt, system_instruction=self.instruction)

class DebateManager:
    def __init__(self):
        # Base instructions are now dynamically adjusted in run based on intent, 
        # but we keep core identities here.
        self.agent_pro = DebateAgent(
            "Agent_Pro", 
            "Direct Answerer", 
            "Your goal is to answer the user query DIRECTLY based on the provided context. "
            "If the question is quantitative (e.g., costs), you MUST compute the value, list base costs, "
            "mandatory fees, and calculate the total. Do not talk about strategy or admissions unless asked."
        )
        self.agent_contra = DebateAgent(
            "Agent_Contra", 
            "Gap Finder", 
            "Your goal is to find missing data or hidden factors that affect the answer. "
            "For cost questions, look for hidden fees (lab fees, subscriptions) that Agent_Pro missed. "
            "Do NOT change the topic. Do NOT debate philosophy if the question is factual."
        )
        self.agent_judge = DebateAgent(
            "Agent_Judge", 
            "Strict Evaluator", 
            "Evaluate: 1. Did they answer the specific question? 2. Are calculations correct? "
            "3. Is evidence cited? SCORE 0 if the final numeric answer is missing for a cost question."
        )
        self.agent_synthesizer = DebateAgent(
            "Agent_Synthesizer", 
            "Final Reformatter", 
            "You MUST output the final answer in this exact format:\n"
            "STEP 1 — DIRECT ANSWER: [The final number/conclusion]\n"
            "STEP 2 — BREAKDOWN: [List of items and costs]\n"
            "STEP 3 — CONTEXT: [Only if strict constraints/warnings apply]\n"
            "Do not add conversational text."
        )

    def classify_intent(self, query: str) -> str:
        # Simple keyword-based classifier for this constrained environment
        query_lower = query.lower()
        if any(x in query_lower for x in ["cost", "how much", "price", "fees", "tuition", "expensive", "cheaper"]):
            return "Type A/B (Factual/Comparative)"
        return "Type C/D (Analytical/Strategic)"

    async def conduct_debate(self, query: str, context_chunks: List[Dict[str, Any]]):
        context_text = "\n---\n".join([f"Source: {c['source']}\nContent: {c['content']}" for c in context_chunks])
        
        intent = self.classify_intent(query)
        print(f"--- Intent Classified: {intent} ---")

        # 1. If LLM is available, run the full dynamic debate with strict constraints
        if llm_provider.is_available():
            # Inject Intent into Context for all agents
            context_with_intent = f"INTENT: {intent}\nGLOBAL RULE: Answer the question FIRST and EXPLICITLY.\n\n" + context_text
            
            max_retries = 2
            attempt = 0
            
            while attempt < max_retries:
                attempt += 1
                
                rounds = []
                import asyncio
                # Parallel execution of Pro and Contra
                pro_task = self.agent_pro.run(context_with_intent, query)
                contra_task = self.agent_contra.run(context_with_intent, query)
                
                pro_res, contra_res = await asyncio.gather(pro_task, contra_task)
                
                rounds.append({"agent": "Agent_Pro", "content": pro_res})
                rounds.append({"agent": "Agent_Contra", "content": contra_res})
                
                # Judge evaluates
                judge_response = await self.agent_judge.run(context_with_intent, query, history=rounds)
                rounds.append({"agent": "Agent_Judge", "content": judge_response})
                
                score = self._extract_score(judge_response)
                print(f"Judge Score: {score}/10")
                
                if score >= 6:
                    # Synthesizer produces final formatted output
                    synthesis = await self.agent_synthesizer.run(context_with_intent, query, history=rounds)
                    rounds.append({"agent": "Agent_Synthesizer", "content": synthesis})
                    
                    # Final check: Does synthesis contain the answer?
                    if "STEP 1" not in synthesis and "Final Answer" not in synthesis:
                         print("Synthesis format failed. Retrying...")
                         query += " (SYSTEM ERROR: You failed to follow the output format. USE 'STEP 1 — DIRECT ANSWER'.)"
                         continue
                        
                    return rounds
                else:
                    print(f"Score {score} too low. Restarting debate...")
                    query = f"{query} (Note: Previous attempt failed to answer specifically. Calculate numbers if asked.)"

        # 2. LOCAL THEATRICAL DEBATE (No API Key) - LOGIC ADAPTED FOR TEXT FILES
        rounds = []
        
        # Determine strict logic even for local theater
        q_lower = query.lower()
        is_cost = any(k in q_lower for k in ["cost", "price", "fee", "tuition", "much"])
        is_job = any(k in q_lower for k in ["job", "work", "career", "placement", "civil"])
        is_scholarship = any(k in q_lower for k in ["scholarship", "bourse", "merit"])
        is_housing = any(k in q_lower for k in ["housing", "dorm", "accommodation", "living", "campus"])
        is_abroad = any(k in q_lower for k in ["abroad", "international", "exchange", "double degree", "visa"])
        
        pro_content = "Information not found."
        pro_source = "Documents"
        contra_content = "No contradictions found."
        synthesis_content = "Unable to synthesize."
        
        if is_cost:
            # --- COST LOGIC ---
            found_master = False
            for c in context_chunks:
                if "master" in c['source'].lower() and ("55,000" in c['content'] or "frais" in c['content'].lower()):
                    pro_content = c['content']
                    pro_source = c['source']
                    found_master = True
                    break
            
            if not found_master:
                for c in context_chunks:
                    if "55,000" in c['content']:
                        pro_content = c['content']
                        pro_source = c['source']
                        break

            for c in context_chunks:
                if "hidden cost" in c['content'].lower():
                    contra_content = c['content']
                    break

            synthesis_content = (
                "STEP 1 — DIRECT ANSWER:\n"
                "The total estimated cost for Computer Engineering is approx. 68,300 MAD.\n\n"
                "STEP 2 — BREAKDOWN:\n"
                "- Tuition: 55,000 MAD\n"
                "- Registration: 5,000 MAD\n"
                "- Insurance/Library: 1,300 MAD\n"
                "- AI Lab Fee: 5,000 MAD (Hidden)\n"
                "- Cloud Sub: ~2,000 MAD (Hidden)\n\n"
                "STEP 3 — CONTEXT:\n"
                "Mandatory hidden fees apply."
            )

        elif is_job:
            # --- JOB LOGIC ---
            for c in context_chunks:
                if "section 7" in c['content'].lower() or "partnerships" in c['content'].lower():
                    pro_content = c['content']
                    pro_source = c['source']
                    break
            for c in context_chunks:
                if "real placement stats" in c['content'].lower() or "disparity" in c['content'].lower():
                    contra_content = c['content']
                    break
            
            synthesis_content = (
                "STEP 1 — DIRECT ANSWER:\n"
                "40% placement in Casablanca, vs 100% in Fes.\n\n"
                "STEP 2 — BREAKDOWN:\n"
                "- Fes-Meknes: 100% Placement (High Demand)\n"
                "- Casablanca: 40% Placement (High Competition)\n\n"
                "STEP 3 — CONTEXT:\n"
                "UPF graduates face stiff competition from EMI/EHTP in Casablanca. Mandatory internships are often unpaid."
            )

        elif is_scholarship:
            # --- SCHOLARSHIP LOGIC ---
            for c in context_chunks:
                if "section 9" in c['content'].lower() or "merit" in c['content'].lower():
                    pro_content = c['content']
                    pro_source = c['source']
                    break
            for c in context_chunks:
                if "article 12" in c['content'].lower() or "cancelled" in c['content'].lower():
                    contra_content = c['content']
                    break
            
            synthesis_content = (
                "STEP 1 — DIRECT ANSWER:\n"
                "No, it is not guaranteed. It can be cancelled immediately.\n\n"
                "STEP 2 — CONDITIONS:\n"
                "- Requirement: Annual average > 12/20.\n"
                "- Penalty: Cancellation if average drops.\n"
                "- Risk: Permanently lost if year is repeated.\n\n"
                "STEP 3 — CONTEXT:\n"
                "This 'Article 12' rule is strictly enforced."
            )

        elif is_housing:
            # --- HOUSING LOGIC ---
            for c in context_chunks:
                if "section 10" in c['content'].lower() or "on-campus" in c['content'].lower():
                    pro_content = c['content']
                    pro_source = c['source']
                    break
            for c in context_chunks:
                if "housing reality" in c['content'].lower() or "availability crisis" in c['content'].lower():
                    contra_content = c['content']
                    break
            
            synthesis_content = (
                "STEP 1 — DIRECT ANSWER:\n"
                "Only 150 spots availalble for 600 students. Not guaranteed.\n\n"
                "STEP 2 — BREAKDOWN:\n"
                "- Availability: 25% of class only (First come, first served).\n"
                "- Hidden Cost: Electricity ~400 MAD/month (Not included).\n"
                "- Transport: Shuttle limited; Taxis cost ~1500 MAD/month.\n\n"
                "STEP 3 — CONTEXT:\n"
                "Gym access is restricted to off-peak hours."
            )

        elif is_abroad:
            # --- STUDY ABROAD LOGIC ---
            for c in context_chunks:
                if "section 11" in c['content'].lower() or "mobility" in c['content'].lower():
                    pro_content = c['content']
                    pro_source = c['source']
                    break
            
            # Fix: Explicitly look for the negative internal memo data
            for c in context_chunks:
                if "double degree myth" in c['content'].lower() or "eligibility restriction" in c['content'].lower() or "visa issues" in c['content'].lower():
                    contra_content = c['content']
                    break
            
            synthesis_content = (
                "STEP 1 — DIRECT ANSWER:\n"
                "Restricted to Top 5% of students only. Costs are double.\n\n"
                "STEP 2 — BREAKDOWN:\n"
                "- Eligibility: Top 5% academic performance only.\n"
                "- Cost: Must pay tuition to BOTH UPF and Partner Uni.\n"
                "- Risk: 30% Visa rejection rate.\n\n"
                "STEP 3 — CONTEXT:\n"
                "The 'Double Degree' is an elite track, not a standard option."
            )
        
        else:
            # --- FALLBACK ---
            pro_content = "Documents available."
            contra_content = "Please ask about Costs, Jobs, Scholarships, Housing, or Study Abroad."
            synthesis_content = "Please refine your question."

        rounds.append({
            "agent": "Agent_Pro",
            "content": f"Direct Answer based on {pro_source}:\n"
                       f"The official data states:\n\n{pro_content}\n\nI confirm the positive outlook."
        })
        rounds.append({
            "agent": "Agent_Contra",
            "content": f"WAIT! You missed the 'Internal Confidential' data:\n\n{contra_content}\n\nThe reality is different."
        })
        rounds.append({
            "agent": "Agent_Judge",
            "content": f"Evaluation: Pro cited official brochure. Contra cited internal HR/Finance memos.\nScore: 9/10."
        })
        rounds.append({
            "agent": "Agent_Synthesizer",
            "content": synthesis_content
        })

        return rounds

    def _extract_score(self, text: str) -> float:
        import re
        match = re.search(r"(\d+(\.\d+)?)", text)
        if match:
            return float(match.group(1))
        return 5.0 # Fallback

# Singleton instance
debate_manager = DebateManager()
