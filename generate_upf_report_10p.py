
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle

def generate_full_report(output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Custom styles
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1, # Center
        textColor=colors.black
    )
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=10,
        textColor=colors.darkblue
    )
    body_style = styles['BodyText']
    body_style.fontSize = 10
    body_style.leading = 14

    # --- PAGE 1: COVER ---
    elements.append(Spacer(1, 100))
    elements.append(Paragraph("UNIVERSITÉ PRIVÉE DE FÈS (UPF)", title_style))
    elements.append(Paragraph("RAPPORT COMPLET D'INTELLIGENCE ET STRATÉGIE 2024-2025", ParagraphStyle('SubTitle', alignment=1, fontSize=14)))
    elements.append(Spacer(1, 200))
    elements.append(Paragraph("Document de Référence pour le Système Débat Core RAG", body_style))
    elements.append(Paragraph("Version: 2.0 (Augmentée)", body_style))
    elements.append(PageBreak())

    # --- PAGE 2: INTRODUCTION & OVERVIEW ---
    elements.append(Paragraph("1. Présentation de l'Institution", section_style))
    elements.append(Paragraph(
        "Fondée en 2006, l'Université Privée de Fès (UPF) s'est imposée comme un pôle d'excellence dans le centre du Maroc. "
        "Reconnue par l'État, elle délivre des diplômes équivalents à ceux du public, un point de débat souvent soulevé par les étudiants. "
        "L'UPF se compose de plusieurs facultés et écoles spécialisées, notamment la Faculté des Sciences de l'Ingénieur, "
        "la Fès Business School, la Faculté de Droit, et l'École d'Architecture. "
        "L'université axe sa stratégie sur 'L'Ingénierie de Demain', intégrant massivement l'IA et les énergies renouvelables.",
        body_style
    ))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(
        "Ce rapport compile les données techniques, administratives et financières pour permettre une analyse multicouche par agents intelligents.",
        body_style
    ))
    elements.append(PageBreak())

    # --- PAGE 3: FACULTE DES SCIENCES DE L'INGENIEUR ---
    elements.append(Paragraph("2. Zoom sur la Faculté des Sciences de l'Ingénieur", section_style))
    elements.append(Paragraph(
        "La Faculté des Sciences de l'Ingénieur est le cœur technologique de l'UPF. Elle propose des cycles d'ingénieur en :",
        body_style
    ))
    elements.append(Paragraph("• Génie Informatique (Spécialités : Big Data, IA, Cybersécurité)", body_style))
    elements.append(Paragraph("• Génie Civil (Spécialités : Bâtiment, Routes, Ouvrages d'art)", body_style))
    elements.append(Paragraph("• Génie Énergétique et Énergies Renouvelables", body_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(
        "Chaque programme dure 5 ans (2 ans de prépa intégrée + 3 ans de cycle ingénieur). "
        "Le cycle est sanctionné par un diplôme d'ingénieur d'État après une soutenance de PFE (Projet de Fin d'Études).",
        body_style
    ))
    elements.append(PageBreak())

    # --- PAGE 4: FOCUS IA ET DATA SCIENCE ---
    elements.append(Paragraph("3. Intelligence Artificielle et Innovation (AII)", section_style))
    elements.append(Paragraph(
        "Le département AII (Artificial Intelligence & Innovation) est le fleuron de l'UPF. "
        "Il dispose de laboratoires équipés de GPU haute performance pour le Deep Learning. "
        "Cependant, l'accès à ces ressources est soumis à une 'AI Lab Fee' de 5,000 MAD par an, un détail souvent omis lors des inscriptions. "
        "Les modules incluent : Neural Networks, Computer Vision, Natural Language Processing, et Éthique de l'IA.",
        body_style
    ))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(
        "DEBAT POSSIBLE : L'université prône l'accès à la technologie pour tous, mais facture des frais supplémentaires pour les ressources de calcul.",
        body_style
    ))
    elements.append(PageBreak())

    # --- PAGE 5: ECOLE D'ARCHITECTURE ET DESIGN ---
    elements.append(Paragraph("4. École d'Architecture et des Métiers du Bâtiment", section_style))
    elements.append(Paragraph(
        "L'Architecture à l'UPF est un cursus de 6 ans, extrêmement exigeant. "
        "Les frais de scolarité sont les plus élevés de l'université (hors dentaire), s'élevant à 75,000 MAD par an. "
        "Les étudiants bénéficient d'ateliers de design ouverts 24/7, mais les frais de maquettes et de matériel sont entièrement à la charge de l'étudiant. "
        "L'école met l'accent sur l'architecture durable et le BIM (Building Information Modeling).",
        body_style
    ))
    elements.append(PageBreak())

    # --- PAGE 6: ADMISSIONS ET CRITERES DE SELECTION ---
    elements.append(Paragraph("5. Processus d'Admission et Sélection", section_style))
    elements.append(Paragraph(
        "L'admission se fait en trois étapes :",
        body_style
    ))
    elements.append(Paragraph("1. Étude de dossier : Moyenne pondérée du Bac (Maths/Physique).", body_style))
    elements.append(Paragraph("2. Test Technique : Épreuve de logique et de culture générale scientifique.", body_style))
    elements.append(Paragraph("3. Entretien : Évaluation de la motivation et du niveau de langue.", body_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(
        "POINT DE FRICTION : Une mention 'Très Bien' dispense du test technique, mais pas de l'entretien de motivation. "
        "Les bourses de mérite (jusqu'à 50%) sont réévaluées chaque année selon les résultats académiques. Si la moyenne descend sous 12/20, la bourse est annulée.",
        body_style
    ))
    elements.append(PageBreak())

    # --- PAGE 7: FINANCES ET TARIFS DETAILLES ---
    elements.append(Paragraph("6. Tarification et Frais Annexes", section_style))
    data = [
        ['Programme', 'Frais Annuels', 'Frais d\'inscription'],
        ['Génie Informatique', '55,000 MAD', '5,000 MAD'],
        ['Génie Civil', '52,000 MAD', '5,000 MAD'],
        ['Architecture', '75,000 MAD', '6,000 MAD'],
        ['Business School', '48,000 MAD', '4,000 MAD'],
        ['Médecine Dentaire', '110,000 MAD', '10,000 MAD'],
    ]
    t = Table(data, colWidths=[200, 150, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(
        "ATTENTION : Ces tarifs n'incluent pas l'assurance obligatoire (800 MAD) et les frais de bibliothèque (500 MAD).",
        body_style
    ))
    elements.append(PageBreak())

    # --- PAGE 8: INSERTION PROFESSIONNELLE ET PARTENARIATS ---
    elements.append(Paragraph("7. Insertion Professionnelle", section_style))
    elements.append(Paragraph(
        "L'UPF revendique un taux d'insertion de 90%. Des partenariats avec des banques (BMCE, Attijari) et des entreprises tech (Oracle, Huawei) facilitent les stages. "
        "Toutefois, le département Civil Engineering subit un ralentissement dû au marché immobilier local, avec un taux de 70% d'insertion après 1 an. "
        "L'IA est le secteur le plus porteur avec des salaires de débutants de 10,000 - 14,000 MAD.",
        body_style
    ))
    elements.append(PageBreak())

    # --- PAGE 9: INFRASTRUCTURE ET ECO-CAMPUS ---
    elements.append(Paragraph("8. Campus et Infrastructures", section_style))
    elements.append(Paragraph(
        "Le campus s'étend sur plusieurs hectares à la Route Ain Chkef. "
        "Equipements : Bibliothèque de 10,000 volumes, Salle de sport, Espace Coworking, Labs de robotique. "
        "NOTE DE CHANTIER : L'extension prévue pour 2024 a pris du retard. Les nouveaux dortoirs ne seront opérationnels qu'en Mars 2025. "
        "Les étudiants actuels doivent loger en ville ou dans des résidences partenaires.",
        body_style
    ))
    elements.append(PageBreak())

    # --- PAGE 10: SYNTHESE DES DEBATS POUR L'IA ---
    elements.append(Paragraph("9. Synthèse pour Débat Multi-Agents", section_style))
    elements.append(Paragraph(
        "Questions de réflexion pour les agents :",
        body_style
    ))
    elements.append(Paragraph("• Le coût de la Médecine Dentaire (110k) est-il justifié par rapport à l'Ingénierie ?", body_style))
    elements.append(Paragraph("• L'obligation de présence physique à 100% en architecture est-elle archaïque à l'ère du digital ?", body_style))
    elements.append(Paragraph("• Les bourses de mérite sont-elles un outil de soutien ou un outil de pression ?", body_style))
    elements.append(Paragraph("• Quel est l'impact réel des retards de chantier sur l'expérience étudiante ?", body_style))
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("FIN DU RAPPORT - UPF STRATEGIC AGENT SOURCE", ParagraphStyle('End', alignment=1, fontSize=12)))

    doc.build(elements)
    print(f"Rapport complet de 10 pages généré avec succès dans {output_path}")

if __name__ == "__main__":
    kb_dir = os.path.join(os.getcwd(), "knowledge_base")
    pdf_path = os.path.join(kb_dir, "UPF_Master_Report_10_Pages.pdf")
    generate_full_report(pdf_path)
