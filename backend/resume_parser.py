import fitz  # PyMuPDF
import re
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
from matcher import match_jobs

@dataclass
class ContactInfo:
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    other_links: List[str] = None

    def __post_init__(self):
        if self.other_links is None:
            self.other_links = []

@dataclass
class Education:
    degree: Optional[str] = None
    institution: Optional[str] = None
    year: Optional[str] = None
    gpa: Optional[str] = None

@dataclass
class Experience:
    title: Optional[str] = None
    company: Optional[str] = None
    duration: Optional[str] = None
    description: Optional[str] = None

@dataclass
class ParsedResume:
    contact_info: ContactInfo
    skills: List[str]
    education: List[Education]
    experience: List[Experience]
    summary: Optional[str] = None

class ResumeParser:
    def __init__(self):
        # Common skill keywords
        self.skill_keywords = [
            # Programming languages
            'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin',
            'go', 'rust', 'scala', 'r', 'matlab', 'sql', 'html', 'css', 'typescript',
            
            # Frameworks and libraries
            'react', 'angular', 'vue', 'django', 'flask', 'spring', 'nodejs', 'express',
            'bootstrap', 'jquery', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'scikit-learn',
            
            # Databases
            'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite', 'cassandra',
            
            # Tools and technologies
            'git', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'jenkins', 'ansible',
            'terraform', 'linux', 'unix', 'bash', 'powershell', 'jira', 'confluence',
            
            # Methodologies
            'agile', 'scrum', 'kanban', 'devops', 'ci/cd', 'tdd', 'bdd'
        ]
        
        # Regex patterns
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        self.linkedin_pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/in/[\w\-]+/?'
        self.github_pattern = r'(?:https?://)?(?:www\.)?github\.com/[\w\-]+/?'
        
        # Education patterns
        self.degree_patterns = [
            r'(?:bachelor|master|phd|doctorate|associate|diploma|certificate|b\.?[as]|m\.?[as]|ph\.?d)',
            r'(?:computer science|engineering|mathematics|physics|chemistry|biology)',
            r'(?:business administration|management|finance|economics|accounting)'
        ]
        
        # Experience patterns
        self.experience_patterns = [
            r'(?:software engineer|developer|programmer|analyst|manager|director|coordinator)',
            r'(?:intern|junior|senior|lead|principal|chief|head)',
            r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+\d{4}'
        ]

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF using PyMuPDF."""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text()
                
            doc.close()
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")

    def extract_links_from_pdf(self, pdf_path: str) -> List[Dict]:
        """Extract all links from PDF including their associated text and coordinates."""
        try:
            doc = fitz.open(pdf_path)
            all_links = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                links = page.get_links()
                
                for link in links:
                    link_info = {
                        'page': page_num,
                        'rect': link['from'],  # coordinates
                        'uri': link.get('uri', ''),
                        'text': ''
                    }
                    
                    # Extract text at the link coordinates
                    rect = fitz.Rect(link['from'])
                    # Expand rectangle slightly to capture text
                    expanded_rect = fitz.Rect(
                        rect.x0 - 5, rect.y0 - 5, 
                        rect.x1 + 5, rect.y1 + 5
                    )
                    
                    # Get text within the link area
                    text_instances = page.get_text("dict", clip=expanded_rect)
                    link_text = ""
                    for block in text_instances.get("blocks", []):
                        if "lines" in block:
                            for line in block["lines"]:
                                for span in line["spans"]:
                                    link_text += span["text"]
                    
                    link_info['text'] = link_text.strip()
                    all_links.append(link_info)
            
            doc.close()
            return all_links
        except Exception as e:
            raise Exception(f"Error extracting links from PDF: {str(e)}")

    def extract_text_and_links_from_pdf(self, pdf_path: str) -> tuple:
        """Extract both text and links from PDF."""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            all_links = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Extract text
                text += page.get_text()
                
                # Extract links
                links = page.get_links()
                for link in links:
                    link_info = {
                        'page': page_num,
                        'rect': link['from'],
                        'uri': link.get('uri', ''),
                        'text': ''
                    }
                    
                    # Extract text at link coordinates
                    rect = fitz.Rect(link['from'])
                    expanded_rect = fitz.Rect(
                        rect.x0 - 5, rect.y0 - 5, 
                        rect.x1 + 5, rect.y1 + 5
                    )
                    
                    text_instances = page.get_text("dict", clip=expanded_rect)
                    link_text = ""
                    for block in text_instances.get("blocks", []):
                        if "lines" in block:
                            for line in block["lines"]:
                                for span in line["spans"]:
                                    link_text += span["text"]
                    
                    link_info['text'] = link_text.strip()
                    all_links.append(link_info)
            
            doc.close()
            return text, all_links
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")

    def extract_contact_info(self, text: str, links: List[Dict] = None) -> ContactInfo:
        """Extract contact information from text and embedded links."""
        contact = ContactInfo()
        
        # Extract from regular text first
        # Extract email
        email_match = re.search(self.email_pattern, text, re.IGNORECASE)
        if email_match:
            contact.email = email_match.group()
        
        # Extract phone
        phone_match = re.search(self.phone_pattern, text)
        if phone_match:
            contact.phone = phone_match.group()
        
        # Extract LinkedIn
        linkedin_match = re.search(self.linkedin_pattern, text, re.IGNORECASE)
        if linkedin_match:
            contact.linkedin = linkedin_match.group()
        
        # Extract GitHub
        github_match = re.search(self.github_pattern, text, re.IGNORECASE)
        if github_match:
            contact.github = github_match.group()
        
        # Extract from embedded links
        if links:
            for link in links:
                uri = link.get('uri', '').lower()
                link_text = link.get('text', '').lower()
                
                # Check for email in links
                if 'mailto:' in uri and not contact.email:
                    contact.email = uri.replace('mailto:', '')
                elif re.search(self.email_pattern, uri, re.IGNORECASE) and not contact.email:
                    email_match = re.search(self.email_pattern, uri, re.IGNORECASE)
                    contact.email = email_match.group()
                
                # Check for LinkedIn
                if 'linkedin.com' in uri and not contact.linkedin:
                    contact.linkedin = link['uri']
                elif 'linkedin' in link_text and 'http' in uri and not contact.linkedin:
                    contact.linkedin = link['uri']
                
                # Check for GitHub
                if 'github.com' in uri and not contact.github:
                    contact.github = link['uri']
                elif 'github' in link_text and 'http' in uri and not contact.github:
                    contact.github = link['uri']
                
                # Check for portfolio/personal websites
                if ('portfolio' in link_text or 'website' in link_text or 
                    link_text.strip() == '' and 'http' in uri) and not contact.portfolio:
                    # Filter out common social media/job sites to find personal sites
                    excluded_domains = ['linkedin', 'github', 'twitter', 'facebook', 'instagram', 
                                      'indeed', 'glassdoor', 'monster', 'careerbuilder']
                    if not any(domain in uri.lower() for domain in excluded_domains):
                        contact.portfolio = link['uri']
                
                # Collect other professional links
                if ('http' in uri and 
                    uri not in [contact.linkedin, contact.github, contact.portfolio] and
                    'mailto:' not in uri and 'tel:' not in uri):
                    contact.other_links.append(link['uri'])
        
        # Extract name (first two words of first line, heuristic)
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line and len(line.split()) >= 2:
                words = line.split()
                if len(words) >= 2 and all(word.replace('.', '').isalpha() for word in words[:2]):
                    contact.name = ' '.join(words[:2])
                    break
        
        return contact

    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text."""
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.skill_keywords:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        # Remove duplicates while preserving order
        return list(dict.fromkeys(found_skills))

    def extract_education(self, text: str) -> List[Education]:
        """Extract education information from text."""
        education_list = []
        lines = text.split('\n')
        
        education_section = False
        current_education = None
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
                
            # Check if we're in education section
            if re.search(r'\b(education|academic|qualification|degree)\b', line, re.IGNORECASE):
                education_section = True
                continue
            
            # Stop if we hit another section
            if education_section and re.search(r'\b(experience|work|employment|project|skill)\b', line, re.IGNORECASE):
                education_section = False
            
            if education_section:
                # Look for institution names first (more specific patterns)
                if re.search(r'\b(university|college|institute|school|iit|nit|bits)\b', line, re.IGNORECASE):
                    if current_education:
                        education_list.append(current_education)
                    current_education = Education()
                    current_education.institution = line
                    
                    # Look for date range in the same line
                    date_match = re.search(r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+\d{4}\s*-\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?\w*\s*\d{4}\b', line, re.IGNORECASE)
                    if not date_match:
                        date_match = re.search(r'\b\d{4}\s*-\s*\d{4}\b', line)
                    if date_match:
                        current_education.year = date_match.group()
                    
                    # Look for degree in the next line
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line and re.search(r'\b(b\.?tech|m\.?tech|bachelor|master|b\.?sc|m\.?sc|b\.?a|m\.?a|phd|diploma|certificate)\b', next_line, re.IGNORECASE):
                            current_education.degree = next_line
                
                # Look for degree patterns
                elif re.search(r'\b(b\.?tech|m\.?tech|bachelor|master|b\.?sc|m\.?sc|b\.?a|m\.?a|phd|diploma|certificate)\b', line, re.IGNORECASE):
                    if not current_education:
                        current_education = Education()
                    if not current_education.degree:
                        current_education.degree = line
                
                # Look for years/dates
                year_match = re.search(r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+\d{4}\s*-\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?\w*\s*\d{4}\b', line, re.IGNORECASE)
                if not year_match:
                    year_match = re.search(r'\b\d{4}\s*-\s*\d{4}\b', line)
                if not year_match:
                    year_match = re.search(r'\b(19|20)\d{2}\b', line)
                    
                if year_match and current_education and not current_education.year:
                    current_education.year = year_match.group()
                
                # Look for GPA/CGPA
                gpa_match = re.search(r'\b(gpa|cgpa)\s*:?\s*(\d+\.?\d*)\s*/?\s*(\d+\.?\d*)\b', line, re.IGNORECASE)
                if gpa_match and current_education:
                    current_education.gpa = gpa_match.group()
        
        if current_education:
            education_list.append(current_education)
        
        return education_list

    def extract_experience(self, text: str) -> List[Experience]:
        """Extract work experience from text."""
        experience_list = []
        lines = text.split('\n')
        
        experience_section = False
        current_experience = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if we're in experience section
            if re.search(r'\b(experience|employment|work|career|professional)\b', line, re.IGNORECASE):
                experience_section = True
                continue
            
            # Stop if we hit another section
            if experience_section and re.search(r'\b(education|skill|project|certification)\b', line, re.IGNORECASE):
                experience_section = False
            
            if experience_section:
                # Look for job titles
                for pattern in self.experience_patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        if current_experience:
                            experience_list.append(current_experience)
                        current_experience = Experience()
                        current_experience.title = line
                        break
                
                # Look for company names (lines that might contain company info)
                if current_experience and not current_experience.company:
                    if re.search(r'\b(inc|corp|ltd|llc|company|technologies|solutions)\b', line, re.IGNORECASE):
                        current_experience.company = line
                
                # Look for duration
                if re.search(r'\b\d{4}\b', line) and current_experience:
                    current_experience.duration = line
        
        if current_experience:
            experience_list.append(current_experience)
        
        return experience_list

    def extract_summary(self, text: str) -> Optional[str]:
        """Extract summary/objective from text."""
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if re.search(r'\b(summary|objective|profile|about)\b', line, re.IGNORECASE):
                # Get next few lines as summary
                summary_lines = []
                for j in range(i+1, min(i+5, len(lines))):
                    next_line = lines[j].strip()
                    if next_line and not re.search(r'\b(education|experience|skill)\b', next_line, re.IGNORECASE):
                        summary_lines.append(next_line)
                    else:
                        break
                
                if summary_lines:
                    return ' '.join(summary_lines)
        
        return None

    def parse_resume(self, pdf_path: str) -> ParsedResume:
        """Parse a resume PDF and extract structured information."""
        # Extract both text and links
        print(f"Parsing resume from: {pdf_path}")
        text, links = self.extract_text_and_links_from_pdf(pdf_path)
        
        contact_info = self.extract_contact_info(text, links)
        skills = self.extract_skills(text)
        education = self.extract_education(text)
        experience = self.extract_experience(text)
        summary = self.extract_summary(text)
        
        return ParsedResume(
            contact_info=contact_info,
            skills=skills,
            education=education,
            experience=experience,
            summary=summary
        )

    def print_extracted_links(self, pdf_path: str):
        """Utility method to print all extracted links for debugging."""
        links = self.extract_links_from_pdf(pdf_path)
        print("=== EXTRACTED LINKS ===")
        for i, link in enumerate(links):
            print(f"Link {i+1}:")
            print(f"  URI: {link['uri']}")
            print(f"  Text: '{link['text']}'")
            print(f"  Page: {link['page']}")
            print(f"  Coordinates: {link['rect']}")
            print()

    def save_parsed_data(self, parsed_resume: ParsedResume, output_path: str):
        """Save parsed resume data to JSON file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(parsed_resume), f, indent=2, ensure_ascii=False)

def main():
    """Example usage of the resume parser."""
    parser = ResumeParser()
    
    # Example usage
    pdf_path = "Ranjeet_Singh_DataScientist.pdf"  # Replace with actual PDF path
    
    try:
        # Parse the resume
        parsed_resume = parser.parse_resume(pdf_path)
        
        # Print results
        print("=== PARSED RESUME ===")
        print(f"Name: {parsed_resume.contact_info.name}")
        print(f"Email: {parsed_resume.contact_info.email}")
        print(f"Phone: {parsed_resume.contact_info.phone}")
        print(f"LinkedIn: {parsed_resume.contact_info.linkedin}")
        print(f"GitHub: {parsed_resume.contact_info.github}")
        print(f"Portfolio: {parsed_resume.contact_info.portfolio}")
        if parsed_resume.contact_info.other_links:
            print(f"Other Links: {', '.join(parsed_resume.contact_info.other_links)}")
        
        print(f"\nSkills: {', '.join(parsed_resume.skills)}")
        
        print("\nEducation:")
        for edu in parsed_resume.education:
            print(f"  - {edu.degree} at {edu.institution} ({edu.year})")
        
        print("\nExperience:")
        for exp in parsed_resume.experience:
            print(f"  - {exp.title} at {exp.company} ({exp.duration})")
        
        if parsed_resume.summary:
            print(f"\nSummary: {parsed_resume.summary}")
        
        # Optional: Print all extracted links for debugging
        print("\n" + "="*50)
        parser.print_extracted_links(pdf_path)
        
        # Save to JSON
        output_path = "parsed_resume.json"
        parser.save_parsed_data(parsed_resume, output_path)
        print(f"\nParsed data saved to {output_path}")

        print('Matching the resume data : ')
        # resume_data = {
        # "summary": parsed_resume["summary"],
        # "skills": parsed_resume["skills"]
        # } 
        matched = match_jobs(parsed_resume)
        print(matched)
        
    except Exception as e:
        print(f"Error parsing resume: {str(e)}")

if __name__ == "__main__":
    main()