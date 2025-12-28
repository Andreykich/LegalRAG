"""Generate synthetic legal documents for demo."""
import json
from pathlib import Path
from src.data_loader import Document

MOCK_DOCUMENTS = [
    {
        "id": "doc_nda_001",
        "title": "Non-Disclosure Agreement Template",
        "content": """
        NON-DISCLOSURE AGREEMENT (NDA)
        
        This Non-Disclosure Agreement ("Agreement") is entered into as of the date of execution 
        between the disclosing party ("Discloser") and the receiving party ("Recipient").
        
        1. CONFIDENTIAL INFORMATION
        Confidential Information means any information disclosed by Discloser to Recipient that 
        is marked as confidential or would reasonably be considered confidential including, 
        but not limited to, trade secrets, business plans, customer lists, and technical data.
        
        2. OBLIGATIONS OF RECIPIENT
        The Recipient agrees to:
        a) Maintain the confidentiality of all Confidential Information received from Discloser
        b) Not disclose Confidential Information to any third parties without prior written consent
        c) Use the Confidential Information solely for the purpose of evaluating the business opportunity
        d) Implement reasonable security measures to protect the Confidential Information
        
        3. EXCLUSIONS
        The following shall not be considered Confidential Information:
        a) Information that is publicly available
        b) Information independently developed without use of Confidential Information
        c) Information received from a third party with the right to disclose
        d) Information required to be disclosed by law or court order
        
        4. TERM AND TERMINATION
        This Agreement shall remain in effect for a period of two (2) years from the date of execution.
        """,
        "source": "legal_templates",
        "metadata": {"type": "nda", "jurisdiction": "US"}
    },
    {
        "id": "doc_service_001",
        "title": "Service Agreement",
        "content": """
        SERVICE AGREEMENT
        
        This Service Agreement ("Agreement") is entered into by and between the Service Provider 
        and the Client for the provision of professional services.
        
        1. SCOPE OF SERVICES
        The Service Provider agrees to provide the following services:
        - Consulting and advisory services
        - Technical implementation support
        - Training and documentation
        - Maintenance and support for 12 months
        
        2. COMPENSATION
        The Client agrees to pay the Service Provider a total fee of $50,000 for the services outlined above.
        Payment shall be made as follows:
        - 50% upon execution of this Agreement
        - 25% upon completion of implementation
        - 25% upon completion of training
        
        3. INTELLECTUAL PROPERTY
        All work product created by the Service Provider shall be owned by the Client.
        The Service Provider retains rights to any pre-existing intellectual property.
        
        4. LIABILITY LIMITATION
        In no event shall either party's liability exceed the total amount paid under this Agreement.
        Neither party shall be liable for indirect, incidental, or consequential damages.
        """,
        "source": "legal_templates",
        "metadata": {"type": "service_agreement", "jurisdiction": "US"}
    },
    {
        "id": "doc_privacy_001",
        "title": "Privacy Policy",
        "content": """
        PRIVACY POLICY
        
        1. INFORMATION WE COLLECT
        We collect information you provide directly to us, such as:
        - Name and contact information
        - Account information
        - Payment information
        - Communication records
        
        2. HOW WE USE YOUR INFORMATION
        We use the information we collect to:
        - Provide and improve our services
        - Communicate with you about our services
        - Process transactions
        - Comply with legal obligations
        
        3. DATA RETENTION
        We retain personal information only as long as necessary to provide services and comply with legal obligations.
        
        4. YOUR RIGHTS
        You have the right to:
        - Access your personal information
        - Correct inaccurate information
        - Request deletion of your information
        - Opt-out of marketing communications
        
        5. SECURITY
        We implement appropriate technical and organizational measures to protect your personal information 
        against unauthorized access, alteration, disclosure, or destruction.
        """,
        "source": "legal_templates",
        "metadata": {"type": "privacy_policy", "jurisdiction": "International"}
    },
    {
        "id": "doc_employment_001",
        "title": "Employment Agreement",
        "content": """
        EMPLOYMENT AGREEMENT
        
        This Employment Agreement is entered into between the Employer and the Employee.
        
        1. POSITION AND DUTIES
        The Employee will be employed in the position of [Position] and shall perform duties 
        as assigned by the Employer, including:
        - [Specific duty 1]
        - [Specific duty 2]
        - [Specific duty 3]
        
        2. COMPENSATION
        The Employee's annual salary is $[Amount], payable in bi-weekly installments.
        The Employee shall be eligible for annual performance reviews and potential salary increases.
        
        3. BENEFITS
        The Employee is entitled to:
        - Health insurance coverage
        - 20 days of paid time off per year
        - 401(k) retirement plan with company match (up to 5%)
        - Professional development allowance
        
        4. TERMINATION
        Employment is at-will and may be terminated by either party with two weeks' written notice.
        Upon termination, the Employee shall receive:
        - Final paycheck for all earned compensation
        - Accrued unused paid time off (where required by law)
        
        5. CONFIDENTIALITY
        The Employee agrees to maintain the confidentiality of all proprietary information 
        and trade secrets of the Employer both during and after employment.
        """,
        "source": "legal_templates",
        "metadata": {"type": "employment_agreement", "jurisdiction": "US"}
    },
    {
        "id": "doc_terms_001",
        "title": "Terms of Service",
        "content": """
        TERMS OF SERVICE
        
        1. ACCEPTANCE OF TERMS
        By accessing or using our website and services, you agree to be bound by these Terms of Service.
        If you do not agree to any portion of these terms, do not use our services.
        
        2. USE LICENSE
        Permission is granted to temporarily download one copy of the materials (information or software) 
        from our website for personal, non-commercial transitory viewing only. This is the grant of a license, 
        not a transfer of title, and under this license you may not:
        - Modify or copy the materials
        - Use the materials for any commercial purpose
        - Attempt to decompile or reverse engineer the software
        - Remove any copyright or proprietary notations
        
        3. DISCLAIMER
        The materials on our website are provided on an 'as is' basis. We make no warranties, expressed or implied, 
        and hereby disclaim and negate all other warranties including, without limitation, implied warranties 
        or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property 
        or other violation of rights.
        
        4. LIMITATIONS
        In no event shall our company be liable for any damages including, without limitation, 
        indirect, incidental, special, consequential, or punitive damages arising out of or relating to 
        these terms or your use of or inability to use our website.
        
        5. MODIFICATIONS TO TERMS
        We reserve the right to modify these terms at any time. Your continued use of the website 
        following the posting of revised terms means that you accept and agree to the changes.
        """,
        "source": "legal_templates",
        "metadata": {"type": "terms_of_service", "jurisdiction": "US"}
    }
]

def generate_mock_documents(count: int = 5) -> list:
    """Generate mock legal documents for testing."""
    docs = []
    for item in MOCK_DOCUMENTS[:count]:
        doc = Document(
            doc_id=item['id'],
            title=item['title'],
            content=item['content'],
            source=item['source'],
            metadata=item['metadata']
        )
        docs.append(doc)
    return docs

def save_mock_data(output_path: Path):
    """Save mock data to JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(MOCK_DOCUMENTS, f, ensure_ascii=False, indent=2)
    print(f"Saved mock data to {output_path}")

if __name__ == "__main__":
    from pathlib import Path
    from src.config import DATA_DIR
    
    output_path = DATA_DIR / "raw" / "sample_legal_docs.json"
    save_mock_data(output_path)
