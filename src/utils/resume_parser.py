import re
from typing import List, Dict, Set
import logging


def clean_line(line: str) -> str:
    """
    Clean and normalize a line of text for better parsing.
    """
    # Remove excessive whitespace
    line = re.sub(r'\s+', ' ', line)
    
    # Remove special characters but keep important ones
    line = re.sub(r'[^\w\s\.\-\+\&\@\#\(\)]', '', line)
    
    return line.strip()


def extract_section_advanced(lines: List[str], section_keywords: List[str]) -> List[str]:
    """
    Advanced section extraction that handles multiple keyword variations.
    """
    section = []
    found_section = False
    
    for i, line in enumerate(lines):
        line_lower = line.lower().strip()
        
        # Check if this line contains any of our section keywords
        if any(keyword in line_lower for keyword in section_keywords):
            found_section = True
            continue
        
        # If we found a section, collect content until next major section
        if found_section:
            # Stop if we hit another major section header
            if is_section_header(line):
                break
            
            # Add non-empty lines
            if line.strip():
                section.append(line.strip())
    
    return [clean_line(line) for line in section if line.strip()]


def extract_section_simple(lines: List[str], section_name: str) -> List[str]:
    """
    Simple section extraction that looks for exact section names.
    """
    section = []
    found_section = False
    
    # Create variations of the section name
    variations = [
        section_name.upper(),
        section_name.title(),
        section_name.lower(),
        f"{section_name.upper()}S",
        f"{section_name.title()}S"
    ]
    
    for line in lines:
        line_clean = line.strip()
        
        # Check if this is our section header
        if any(var in line_clean for var in variations):
            found_section = True
            continue
        
        # If we found a section, collect content until next major section
        if found_section:
            # Stop if we hit another major section header
            if is_section_header(line):
                break
            
            # Add non-empty lines
            if line_clean:
                section.append(line_clean)
    
    return section


def is_section_header(line: str) -> bool:
    """
    Determine if a line is likely a section header.
    """
    line_clean = line.strip()
    
    # Common section headers
    section_headers = {
        'education', 'experience', 'skills', 'projects', 'work', 'employment',
        'academic', 'qualifications', 'certifications', 'languages', 'interests',
        'achievements', 'awards', 'publications', 'references', 'contact'
    }
    
    # Check if line is a known header
    if line_clean.lower() in section_headers:
        return True
    
    # Check if line looks like a header (short, all caps, or bold-like)
    if len(line_clean.split()) <= 4:
        if line_clean.isupper() or re.match(r'^[A-Z][A-Z\s]+$', line_clean):
            return True
    
    return False


def extract_skills_advanced(skill_lines: List[str]) -> List[str]:
    """
    Advanced skill extraction with better handling of various formats.
    """
    skills = set()
    
    for line in skill_lines:
        # Remove category labels (e.g., "Programming Languages:", "Technical Skills:")
        if ':' in line:
            line = line.split(':', 1)[1]
        
        # Handle different separators
        separators = [',', ';', '|', '•', '·', '▪', '▫', '◦', '‣', '⁃']
        
        for sep in separators:
            if sep in line:
                parts = [part.strip() for part in line.split(sep) if part.strip()]
                skills.update(parts)
                break
        else:
            # If no separators found, split by spaces for short terms
            words = line.split()
            if len(words) <= 3:  # Likely individual skills
                skills.add(line.strip())
            else:
                # Try to extract skill-like terms
                skill_terms = extract_skill_terms(line)
                skills.update(skill_terms)
    
    # Clean and filter skills
    cleaned_skills = []
    for skill in skills:
        skill_clean = clean_skill(skill)
        if skill_clean and len(skill_clean) > 1:
            cleaned_skills.append(skill_clean)
    
    return list(dict.fromkeys(cleaned_skills))  # Remove duplicates while preserving order


def extract_skill_terms(text: str) -> List[str]:
    """
    Extract skill-like terms from text using pattern matching.
    """
    skills = []
    
    # Common skill patterns
    patterns = [
        r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',  # CamelCase terms
        r'\b[A-Z]{2,}\b',  # Acronyms
        r'\b[a-z]+\.[a-z]+\b',  # Abbreviations like "m.s."
        r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b',  # Two-word capitalized terms
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        skills.extend(matches)
    
    return skills


def clean_skill(skill: str) -> str:
    """
    Clean and normalize a skill term.
    """
    # Remove common prefixes/suffixes
    skill = re.sub(r'^(and|or|&)\s+', '', skill, flags=re.IGNORECASE)
    skill = re.sub(r'\s+(and|or|&)$', '', skill, flags=re.IGNORECASE)
    
    # Remove version numbers and years
    skill = re.sub(r'\s+\d+\.?\d*', '', skill)
    skill = re.sub(r'\s+\d{4}', '', skill)
    
    # Clean up whitespace
    skill = re.sub(r'\s+', ' ', skill).strip()
    
    return skill


def extract_contact_info(text: str) -> Dict[str, str]:
    """
    Extract contact information from resume text.
    """
    contact_info = {}
    
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_match = re.search(email_pattern, text)
    if email_match:
        contact_info['email'] = email_match.group()
    
    # Phone pattern
    phone_patterns = [
        r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # US format
        r'\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}\b',  # International
    ]
    
    for pattern in phone_patterns:
        phone_match = re.search(pattern, text)
        if phone_match:
            contact_info['phone'] = phone_match.group()
            break
    
    # LinkedIn pattern
    linkedin_pattern = r'linkedin\.com/in/[A-Za-z0-9-]+'
    linkedin_match = re.search(linkedin_pattern, text)
    if linkedin_match:
        contact_info['linkedin'] = linkedin_match.group()
    
    return contact_info


def parse_resume_single_line(raw_text: str) -> Dict[str, any]:
    """
    Specialized parser for resumes that are extracted as a single line.
    Uses regex patterns to extract sections.
    """
    import re
    
    # Extract contact information
    contact_info = extract_contact_info(raw_text)
    
    # Define regex patterns for each section
    patterns = {
        'education': r'EDUCATION\s+(.*?)(?=SKILLS|PROJECTS|CERTIFICATIONS|ACHIEVEMENTS|$)',
        'skills': r'SKILLS\s+(.*?)(?=PROJECTS|CERTIFICATIONS|ACHIEVEMENTS|$)',
        'projects': r'PROJECTS\s+(.*?)(?=CERTIFICATIONS|ACHIEVEMENTS|EXTRACURRICULAR|$)',
        'certifications': r'CERTIFICATIONS\s+(.*?)(?=ACHIEVEMENTS|EXTRACURRICULAR|$)',
        'achievements': r'ACHIEVEMENTS\s+(.*?)(?=EXTRACURRICULAR|$)',
        'extracurricular': r'EXTRACURRICULAR\s+(.*?)$'
    }
    
    parsed_data = {
        'contact': contact_info,
        'education': [],
        'experience': [],
        'projects': [],
        'skills': [],
        'certifications': [],
        'achievements': [],
        'extracurricular': [],
        'raw_text': raw_text
    }
    
    # Extract sections using regex
    for section_name, pattern in patterns.items():
        match = re.search(pattern, raw_text, re.IGNORECASE | re.DOTALL)
        if match:
            section_content = match.group(1).strip()
            
            if section_name == 'skills':
                # Special handling for skills
                skills = extract_skills_from_text(section_content)
                parsed_data[section_name] = skills
            elif section_name == 'projects':
                # Special handling for projects
                projects = extract_projects_from_text(section_content)
                parsed_data[section_name] = projects
            else:
                # For other sections, split by bullet points
                items = extract_bullet_points(section_content)
                parsed_data[section_name] = items
    
    # Add metadata
    parsed_data['metadata'] = {
        'total_characters': len(raw_text),
        'sections_found': [k for k, v in parsed_data.items() if v and k not in ['contact', 'raw_text', 'metadata']],
        'contact_info_found': bool(contact_info)
    }
    
    return parsed_data


def extract_skills_from_text(skills_text: str) -> List[str]:
    """
    Extract skills from the skills section text.
    """
    skills = []
    
    # Split by bullet points first
    bullet_sections = skills_text.split('•')
    
    for section in bullet_sections:
        section = section.strip()
        if not section:
            continue
            
        # Look for category labels (e.g., "Languages:", "Web Development:")
        if ':' in section:
            category, skills_list = section.split(':', 1)
            # Extract skills from the list
            skill_items = extract_skill_items(skills_list)
            skills.extend(skill_items)
        else:
            # No category, treat as individual skills
            skill_items = extract_skill_items(section)
            skills.extend(skill_items)
    
    return list(dict.fromkeys(skills))  # Remove duplicates


def extract_skill_items(text: str) -> List[str]:
    """
    Extract individual skill items from text.
    """
    skills = []
    
    # Split by common separators
    separators = [',', ';', '|', '&']
    
    for sep in separators:
        if sep in text:
            parts = [part.strip() for part in text.split(sep) if part.strip()]
            skills.extend(parts)
            break
    else:
        # If no separators found, split by spaces for short terms
        words = text.split()
        if len(words) <= 5:  # Likely individual skills
            skills.append(text.strip())
        else:
            # Try to extract skill-like terms
            skill_terms = extract_skill_terms(text)
            skills.extend(skill_terms)
    
    return [clean_skill(skill) for skill in skills if clean_skill(skill)]


def extract_projects_from_text(projects_text: str) -> List[str]:
    """
    Extract projects from the projects section text.
    """
    projects = []
    
    # Split by project indicators
    project_indicators = ['§', '•', 'Tools:', 'Mentor:']
    
    # Look for project names (usually followed by § or Tools:)
    project_patterns = [
        r'([A-Z][A-Za-z\s]+)\s*§',  # Project name followed by §
        r'([A-Z][A-Za-z\s]+)\s*Tools:',  # Project name followed by Tools:
    ]
    
    import re
    for pattern in project_patterns:
        matches = re.findall(pattern, projects_text)
        for match in matches:
            project_name = match.strip()
            if len(project_name) > 3:  # Filter out short matches
                projects.append(project_name)
    
    # If no projects found with patterns, try bullet points
    if not projects:
        bullet_sections = projects_text.split('•')
        for section in bullet_sections:
            section = section.strip()
            if section and len(section) > 10:
                projects.append(section)
    
    return list(dict.fromkeys(projects))


def extract_bullet_points(text: str) -> List[str]:
    """
    Extract bullet points from text.
    """
    items = []
    
    # Split by bullet points
    bullet_sections = text.split('•')
    
    for section in bullet_sections:
        section = section.strip()
        if section and len(section) > 5:  # Filter out very short items
            items.append(section)
    
    return items


def parse_resume_enhanced(raw_text: str) -> Dict[str, any]:
    """
    Enhanced resume parsing with better section detection and data extraction.
    """
    # Check if text is mostly on one line (common with PyMuPDF)
    lines = raw_text.split('\n')
    if len(lines) <= 3:  # Single line or very few lines
        return parse_resume_single_line(raw_text)
    
    # Original multi-line parsing logic
    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
    
    # Extract contact information
    contact_info = extract_contact_info(raw_text)
    
    # Try simple section extraction first
    education = extract_section_simple(lines, "EDUCATION")
    experience = extract_section_simple(lines, "EXPERIENCE")
    projects = extract_section_simple(lines, "PROJECTS")
    skills_section = extract_section_simple(lines, "SKILLS")
    
    # If simple extraction didn't work, try advanced
    if not education:
        education = extract_section_advanced(lines, ['education', 'academic', 'qualifications', 'degree', 'university', 'college'])
    
    if not experience:
        experience = extract_section_advanced(lines, ['experience', 'work', 'employment', 'career', 'professional'])
    
    if not projects:
        projects = extract_section_advanced(lines, ['projects', 'project', 'portfolio', 'works', 'achievements'])
    
    if not skills_section:
        skills_section = extract_section_advanced(lines, ['skills', 'technical skills', 'technologies', 'programming', 'languages', 'tools'])
    
    # Extract skills from the skills section
    skills = extract_skills_advanced(skills_section)
    
    # Create parsed data
    parsed_data = {
        'contact': contact_info,
        'education': education,
        'experience': experience,
        'projects': projects,
        'skills': skills,
        'raw_text': raw_text
    }
    
    # Add metadata
    parsed_data['metadata'] = {
        'total_lines': len(lines),
        'sections_found': [k for k, v in {'education': education, 'experience': experience, 'projects': projects, 'skills': skills}.items() if v],
        'contact_info_found': bool(contact_info)
    }
    
    logging.info(f"Parsed resume with {len(skills)} skills, "
                f"{len(projects)} projects, "
                f"{len(education)} education entries")
    
    return parsed_data


def parse_resume(raw_text: str) -> Dict[str, any]:
    """
    Main resume parsing function (backward compatibility).
    """
    return parse_resume_enhanced(raw_text)


def analyze_resume_quality(parsed_data: Dict[str, any]) -> Dict[str, any]:
    """
    Analyze the quality and completeness of parsed resume data.
    """
    analysis = {
        'completeness_score': 0,
        'missing_sections': [],
        'recommendations': [],
        'strengths': []
    }
    
    total_sections = 4  # education, experience, projects, skills
    found_sections = 0
    
    # Check each section
    if parsed_data.get('education'):
        found_sections += 1
        analysis['strengths'].append('Education information found')
    else:
        analysis['missing_sections'].append('Education')
    
    if parsed_data.get('experience'):
        found_sections += 1
        analysis['strengths'].append('Work experience found')
    else:
        analysis['missing_sections'].append('Experience')
    
    if parsed_data.get('projects'):
        found_sections += 1
        analysis['strengths'].append('Project portfolio found')
    else:
        analysis['missing_sections'].append('Projects')
    
    if parsed_data.get('skills'):
        found_sections += 1
        analysis['strengths'].append(f'Skills found ({len(parsed_data["skills"])} skills)')
    else:
        analysis['missing_sections'].append('Skills')
    
    # Calculate completeness score
    analysis['completeness_score'] = (found_sections / total_sections) * 100
    
    # Generate recommendations
    if analysis['completeness_score'] < 75:
        analysis['recommendations'].append('Consider adding missing sections to improve resume completeness')
    
    if len(parsed_data.get('skills', [])) < 5:
        analysis['recommendations'].append('Add more technical skills to showcase your capabilities')
    
    if len(parsed_data.get('projects', [])) < 2:
        analysis['recommendations'].append('Include more projects to demonstrate practical experience')
    
    return analysis


if __name__ == "__main__":
    # Test the enhanced parser
    test_text = """
    JOHN DOE
    john.doe@email.com | (555) 123-4567 | linkedin.com/in/johndoe
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology, 2020-2024
    
    EXPERIENCE
    Software Engineer Intern
    Tech Company Inc., Summer 2023
    • Developed web applications using React and Node.js
    • Collaborated with team of 5 developers
    
    PROJECTS
    AI Chatbot Application
    • Built using Python, TensorFlow, and Flask
    • Implemented natural language processing
    
    SKILLS
    Programming Languages: Python, JavaScript, Java, C++
    Frameworks: React, Node.js, Django, Flask
    Tools: Git, Docker, AWS, MongoDB
    """
    
    result = parse_resume_enhanced(test_text)
    print("Parsed Resume Data:")
    for key, value in result.items():
        if key != 'raw_text':
            print(f"{key}: {value}")
    
    # Analyze quality
    quality = analyze_resume_quality(result)
    print(f"\nQuality Analysis:")
    print(f"Completeness Score: {quality['completeness_score']}%")
    print(f"Strengths: {quality['strengths']}")
    print(f"Recommendations: {quality['recommendations']}")
