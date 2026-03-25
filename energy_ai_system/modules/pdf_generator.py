from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom styles for the PDF report"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue,
            spaceBefore=20
        ))
        
        # Section heading style
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkblue,
            borderWidth=1,
            borderColor=colors.darkblue,
            borderPadding=5
        ))
        
        # Normal text style
        self.styles.add(ParagraphStyle(
            name='CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            leftIndent=20
        ))
    
    def generate_report(self, report_data):
        """Generate PDF report with all prediction results"""
        
        # Create a buffer for the PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        # Build the story (content)
        story = []
        
        # Title
        story.append(Paragraph("AI Data Center Energy Forecast Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 12))
        
        # Generated date/time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        story.append(Paragraph(f"<b>Generated:</b> {current_time}", self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Scenario Details Section
        story.append(Paragraph("Scenario Details", self.styles['SectionHeading']))
        
        scenario_data = [
            ['Parameter', 'Value'],
            ['Scenario Type', report_data.get('scenario_type', 'N/A')],
            ['Workload Scale', f"{report_data.get('workload_scale', 'N/A')}x"],
            ['Temperature Adjustment', f"{report_data.get('temperature_adjustment', 'N/A')}°C"]
        ]
        
        scenario_table = Table(scenario_data, colWidths=[2*inch, 3*inch])
        scenario_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(scenario_table)
        story.append(Spacer(1, 20))
        
        # Energy Prediction Section
        story.append(Paragraph("Energy Prediction", self.styles['SectionHeading']))
        story.append(Paragraph(f"<b>Predicted Energy:</b> {report_data.get('energy', 'N/A')} kWh", self.styles['CustomNormal']))
        story.append(Spacer(1, 15))
        
        # Carbon Emission Section
        story.append(Paragraph("Carbon Emission", self.styles['SectionHeading']))
        story.append(Paragraph(f"<b>Estimated Carbon Emission:</b> {report_data.get('carbon', 'N/A')} kg CO₂", self.styles['CustomNormal']))
        story.append(Spacer(1, 15))
        
        # AI Operational Recommendation Section
        story.append(Paragraph("AI Operational Recommendation", self.styles['SectionHeading']))
        recommendation = report_data.get('recommendation', {})
        if recommendation:
            story.append(Paragraph(f"<b>Status:</b> {recommendation.get('status', 'N/A')}", self.styles['CustomNormal']))
            story.append(Paragraph("<b>Recommendations:</b>", self.styles['CustomNormal']))
            for rec in recommendation.get('recommendations', []):
                story.append(Paragraph(f"• {rec}", self.styles['CustomNormal']))
        story.append(Spacer(1, 15))
        
        # Explainable AI Section
        story.append(Paragraph("Explainable AI - Feature Importance", self.styles['SectionHeading']))
        importance = report_data.get('importance', {})
        if importance:
            for feature, value in importance.items():
                story.append(Paragraph(f"• {feature}: {value:.2f}%", self.styles['CustomNormal']))
        story.append(Paragraph(f"<b>Most Influential Factor:</b> {report_data.get('top_feature', 'N/A')}", self.styles['CustomNormal']))
        story.append(Spacer(1, 15))
        
        # Scenario Comparison Section
        story.append(Paragraph("Scenario Comparison Summary", self.styles['SectionHeading']))
        comparison = report_data.get('comparison', {})
        if comparison:
            comparison_data = [['Scenario', 'Energy (kWh)', 'Carbon (kg CO₂)']]
            for scenario, values in comparison.items():
                comparison_data.append([
                    scenario.title(),
                    f"{values.get('energy', 'N/A')}",
                    f"{values.get('carbon', 'N/A')}"
                ])
            
            comparison_table = Table(comparison_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
            comparison_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(comparison_table)
        story.append(Spacer(1, 15))
        
        # Future Energy Forecast Section
        story.append(Paragraph("Future Energy Forecast (15 Days)", self.styles['SectionHeading']))
        forecast_dates = report_data.get('forecast_dates', [])
        forecast_values = report_data.get('forecast_values', [])
        
        if forecast_dates and forecast_values:
            forecast_data = [['Date', 'Predicted Energy (kWh)']]
            for date, value in zip(forecast_dates, forecast_values):
                forecast_data.append([date, f"{value}"])
            
            forecast_table = Table(forecast_data, colWidths=[2*inch, 2*inch])
            forecast_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(forecast_table)
        
        # AI Forecast Analysis
        if 'forecast_analysis' in report_data:
            story.append(Spacer(1, 10))
            story.append(Paragraph("AI Forecast Analysis", self.styles['SectionHeading']))
            story.append(Paragraph(report_data['forecast_analysis'], self.styles['CustomNormal']))
        
        # Build PDF
        doc.build(story)
        
        # Get PDF from buffer
        buffer.seek(0)
        return buffer.getvalue()
