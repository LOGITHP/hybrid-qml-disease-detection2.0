import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak, Preformatted
)
from reportlab.pdfgen import canvas
import fitz

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, 762, "Hybrid QML Disease Detection Platform — Codebase & Architecture Showcase")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(36, 756, 576, 756)
            
        # Footer
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 42, 576, 42)
        
        self.drawString(36, 30, "Confidential & Proprietary — Research & Development Codebase")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(576, 30, page_str)
        self.restoreState()


def load_code_snippet(filepath, max_lines=45, start_line=1):
    """Safely extracts code snippet from file with formatting."""
    if not os.path.exists(filepath):
        return f"# File not found: {filepath}"
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        subset = lines[start_line-1 : start_line-1 + max_lines]
        # Clean up tabs
        cleaned = [l.replace('\t', '    ') for l in subset]
        return "".join(cleaned).strip()
    except Exception as e:
        return f"# Error reading file: {str(e)}"


def create_code_showcase_pdf(output_path="Project_Code_Showcase.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0F172A'),
        alignment=0
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0D9488'),
        alignment=0
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'ShowcaseBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    code_desc_style = ParagraphStyle(
        'CodeDesc',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#475569'),
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=8.8,
        textColor=colors.HexColor('#0F172A')
    )

    story = []

    # ================= COVER / TITLE SECTION =================
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>HYBRID QML DISEASE DETECTION PLATFORM</b>", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Comprehensive Codebase, Quantum Circuits & Engineering Showcase", subtitle_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#0D9488'), spaceBefore=2, spaceAfter=10))

    meta_table_data = [
        [
            Paragraph("<b>Target System:</b> Full-Stack Quantum-Classical Platform", body_style),
            Paragraph("<b>Quantum SDK:</b> PennyLane (QNode, AngleEmbedding)", body_style)
        ],
        [
            Paragraph("<b>Backend API:</b> FastAPI 0.111+ · MongoDB / Beanie ODM", body_style),
            Paragraph("<b>Autonomous Agent:</b> LangGraph Preprocessing Engine", body_style)
        ],
        [
            Paragraph("<b>Frontend:</b> React 18 · TypeScript · Vite · Tailwind", body_style),
            Paragraph("<b>Deployment:</b> Docker · Nginx · Render PaaS", body_style)
        ]
    ]
    t_meta = Table(meta_table_data, colWidths=[270, 270])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # Architecture Overview
    story.append(Paragraph("<b>Repository Architecture & Directory Hierarchy</b>", h2_style))
    repo_tree = """hybrid-qml-disease-detection/
├── Diseases_Detection_Paltform/       # Core Full-Stack Web Application
│   ├── backend/
│   │   ├── app/
│   │   │   ├── agents/preprocessing_agent/ # AI Preprocessing Pipeline & Tools
│   │   │   ├── api/v1/                     # FastAPI Endpoints (Auth, Datasets, Training, QML)
│   │   │   ├── database/models/            # Beanie ODM MongoDB Document Schemas
│   │   │   ├── ml/                         # PennyLane VQC & Classical SVM Implementations
│   │   │   └── services/                   # Business Services (Dataset, Training, Prediction)
│   │   └── tests/                          # Pytest Unit & Integration Test Suite
│   └── frontend/
│       ├── src/
│       │   ├── api/                        # Strongly Typed Axios Client & Domain Modules
│       │   ├── components/                 # CircuitDesigner, PreprocessingPlan, Navigation
│       │   └── pages/                      # Datasets, Preprocessing, Models, Predictions, Reports
│       └── package.json                    # React 18, Vite, TanStack Query, Tailwind
├── Experimental_ML/Lung_Cancer/        # Research Notebooks, Datasets, Checkpoints & Metrics
├── ai_preprocessing_agent/             # Standalone LangGraph Preprocessing Research Package
├── One_Page_Project_Description.pdf    # Executive Project Summary (Verified 1 Page)
└── README.md                           # Main Documentation, Architecture & Runbook"""
    
    t_tree = Table([[Preformatted(repo_tree, code_style)]], colWidths=[540])
    t_tree.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#38BDF8')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_tree)
    story.append(Spacer(1, 14))

    # ================= SECTION 1: QUANTUM MACHINE LEARNING =================
    story.append(PageBreak())
    story.append(Paragraph("1. Quantum Machine Learning Engine (PennyLane VQC)", h1_style))
    story.append(Paragraph(
        "The core quantum model is a parameterized <b>Variational Quantum Classifier (VQC)</b> built using <b>PennyLane</b>. "
        "It features Y-axis Angle Embedding, strongly entangling parameterized rotation layers, nearest-neighbor CNOT entanglement, "
        "and global Pauli-Z expectation measurement mapped through a calibrated sigmoid classification head.",
        body_style
    ))
    story.append(Paragraph("<b>Source File:</b> <code>Diseases_Detection_Paltform/backend/app/ml/vqc.py</code> (Circuit & QNode Construction)", code_desc_style))

    vqc_code = load_code_snippet(
        "Diseases_Detection_Paltform/backend/app/ml/vqc.py",
        max_lines=38,
        start_line=1
    )
    t_vqc = Table([[Preformatted(vqc_code, code_style)]], colWidths=[540])
    t_vqc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_vqc)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Source File:</b> <code>Diseases_Detection_Paltform/backend/app/ml/vqc.py</code> (Forward Pass & Training Loop)", code_desc_style))
    vqc_train_code = load_code_snippet(
        "Diseases_Detection_Paltform/backend/app/ml/vqc.py",
        max_lines=36,
        start_line=60
    )
    t_vqc_train = Table([[Preformatted(vqc_train_code, code_style)]], colWidths=[540])
    t_vqc_train.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_vqc_train)

    # ================= SECTION 2: CLASSICAL MACHINE LEARNING =================
    story.append(PageBreak())
    story.append(Paragraph("2. Classical Machine Learning Baselines (SVM & Logistic)", h1_style))
    story.append(Paragraph(
        "Classical classifiers establish clinical baselines to benchmark quantum advantages and limitations. "
        "The platform includes Linear SVM, RBF SVM with Gaussian kernels, and regularized Logistic Regression. "
        "Models are evaluated using Stratified 5-Fold Cross-Validation with balanced accuracy optimization.",
        body_style
    ))
    story.append(Paragraph("<b>Source File:</b> <code>Diseases_Detection_Paltform/backend/app/ml/svm.py</code>", code_desc_style))

    svm_code = load_code_snippet(
        "Diseases_Detection_Paltform/backend/app/ml/svm.py",
        max_lines=42,
        start_line=1
    )
    t_svm = Table([[Preformatted(svm_code, code_style)]], colWidths=[540])
    t_svm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_svm)

    # ================= SECTION 3: AI PREPROCESSING AGENT =================
    story.append(PageBreak())
    story.append(Paragraph("3. Autonomous AI Preprocessing Agent", h1_style))
    story.append(Paragraph(
        "The Preprocessing Agent performs automated, schema-aware tabular data preparation with a strict 'split-before-fit' "
        "leakage prevention guarantee. It features automated type inference, missing-value imputation (median/mode), categorical encoding, "
        "outlier clipping, and [0, 1] scaling specifically tailored for quantum state preparation.",
        body_style
    ))
    story.append(Paragraph("<b>Source File:</b> <code>Diseases_Detection_Paltform/backend/app/agents/preprocessing_agent/interface.py</code> (Execution Facade)", code_desc_style))

    prep_code = load_code_snippet(
        "Diseases_Detection_Paltform/backend/app/agents/preprocessing_agent/interface.py",
        max_lines=42,
        start_line=30
    )
    t_prep = Table([[Preformatted(prep_code, code_style)]], colWidths=[540])
    t_prep.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_prep)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Source File:</b> <code>Diseases_Detection_Paltform/backend/app/agents/preprocessing_agent/tools/feature_selection.py</code> (Quantum Feature Budgeting)", code_desc_style))
    feat_code = load_code_snippet(
        "Diseases_Detection_Paltform/backend/app/agents/preprocessing_agent/tools/feature_selection.py",
        max_lines=35,
        start_line=20
    )
    t_feat = Table([[Preformatted(feat_code, code_style)]], colWidths=[540])
    t_feat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_feat)

    # ================= SECTION 4: FASTAPI & BEANIE DATABASE =================
    story.append(PageBreak())
    story.append(Paragraph("4. Enterprise Backend Architecture (FastAPI & Beanie ODM)", h1_style))
    story.append(Paragraph(
        "The asynchronous backend uses FastAPI with Pydantic v2 schemas and Beanie ODM for MongoDB. "
        "It enforces JWT Bearer authentication, role-based access control, dataset multi-user isolation, and complete experiment audit trails.",
        body_style
    ))
    story.append(Paragraph("<b>Source File:</b> <code>Diseases_Detection_Paltform/backend/app/database/models/training.py</code> (Document ODM Models)", code_desc_style))

    db_code = load_code_snippet(
        "Diseases_Detection_Paltform/backend/app/database/models/training.py",
        max_lines=42,
        start_line=1
    )
    t_db = Table([[Preformatted(db_code, code_style)]], colWidths=[540])
    t_db.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_db)

    # ================= SECTION 5: CLINICAL WORKBENCH FRONTEND =================
    story.append(PageBreak())
    story.append(Paragraph("5. Interactive Clinical Workbench (React 18 & TypeScript)", h1_style))
    story.append(Paragraph(
        "The frontend is a single-page application built with React 18, Vite, and Tailwind CSS. "
        "It includes a dynamic Quantum Circuit Designer, guided 7-stage preprocessing pipeline, interactive risk scoring, and TanStack React Query caching.",
        body_style
    ))
    story.append(Paragraph("<b>Source File:</b> <code>Diseases_Detection_Paltform/frontend/src/api/client.ts</code> (JWT Interceptors & Error Handling)", code_desc_style))

    fe_client = load_code_snippet(
        "Diseases_Detection_Paltform/frontend/src/api/client.ts",
        max_lines=42,
        start_line=1
    )
    t_fe_client = Table([[Preformatted(fe_client, code_style)]], colWidths=[540])
    t_fe_client.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_fe_client)

    # ================= SECTION 6: SMOKE TESTING & CLOUD DEPLOYMENT =================
    story.append(PageBreak())
    story.append(Paragraph("6. Verification Testing & Cloud Deployment Runbook", h1_style))
    story.append(Paragraph(
        "The repository includes end-to-end smoke verification scripts (`test_vqc_local.py`), cloud inspection tooling (`fetch_run.py`), "
        "and declarative infrastructure definitions for Docker Compose and Render Cloud.",
        body_style
    ))
    story.append(Paragraph("<b>Source File:</b> <code>test_vqc_local.py</code> (Stand-alone Quantum VQC Unit Verification)", code_desc_style))

    smoke_code = load_code_snippet(
        "test_vqc_local.py",
        max_lines=36,
        start_line=1
    )
    t_smoke = Table([[Preformatted(smoke_code, code_style)]], colWidths=[540])
    t_smoke.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_smoke)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Source File:</b> <code>render.yaml</code> (Render PaaS Multi-Service Infrastructure as Code)", code_desc_style))
    render_code = load_code_snippet(
        "render.yaml",
        max_lines=35,
        start_line=1
    )
    t_render = Table([[Preformatted(render_code, code_style)]], colWidths=[540])
    t_render.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_render)

    doc.build(story, canvasmaker=NumberedCanvas)

    pdf_doc = fitz.open(output_path)
    page_count = len(pdf_doc)
    pdf_doc.close()
    print(f"Generated {output_path} successfully. Total pages: {page_count}")
    return page_count

if __name__ == "__main__":
    count = create_code_showcase_pdf()
    print(f"Code showcase PDF build complete: {count} pages.")
