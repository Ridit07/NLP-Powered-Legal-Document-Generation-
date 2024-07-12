
import base64
import streamlit as st
import spacy
import re
from dateutil.parser import parse



from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag
import language_tool_python

# Initialize language tool and Spacy
tool = language_tool_python.LanguageTool('en-US')
nlp = spacy.load("en_core_web_sm")

# Load the NLP model
nlp = spacy.load("en_core_web_sm")

# import sys
# sys.path.append('/Users/riditjain/Downloads/Active-to-Passive-Voice-master/')

# from act_pas import active_to_passive

# sys.path.append('/Users/riditjain/Downloads/signature_detection-main/')
# from sign1234 import process_pdf_signature


def correct_text(text):
    sentences = sent_tokenize(text)
    corrected_text = []
    for sentence in sentences:
        matches = tool.check(sentence)
        corrected_sentence = language_tool_python.utils.correct(sentence, matches)
        corrected_text.append(corrected_sentence)
    return ' '.join(corrected_text)

def transform_sentence(sentence):
    # Assuming we have a legal_dictionary to convert to legal terms
    legal_dictionary = {
        # Example: 'pay': 'remit',
        # Add more legal synonyms here

         'car': 'motor vehicle',
     'agreement': 'contract',
    'pay': 'remunerate',
    'owner': 'proprietor',
    'agent': 'representative',
    'party': 'party to the agreement',
    'services': 'services rendered',
    'client': 'clientele',
    'consultant': 'advisor',
    'contractor': 'independent contractor',
    'employee': 'staff member',
    'lease': 'leasehold',
    'rent': 'lease payment',
    'payment': 'remittance',
    'fees': 'fee structure',
    'debt': 'financial obligation',
    'loan': 'loaned capital',
    'deadline': 'due date',
    'termination': 'cessation',
    'amendment': 'modification',
    'dispute': 'contention',
    'law': 'statute',
    'right': 'entitlement',
    'duty': 'obligation',
    'responsibility': 'accountability',
    'authority': 'authorized entity',
    'agreement term': 'term of the agreement',
    'effective date': 'date of effectuation',
    'signature': 'endorsement',
    'obligation': 'legal binding',
    'confidentiality': 'nondisclosure',
    'mediation': 'mediatory proceedings',
    'arbitration': 'arbitral process',
    'negotiation': 'deliberative discussions',
    'warranty': 'guaranty',
    'represent': 'represent legally',
    'indemnify': 'hold harmless',
    'breach': 'violation',
    'compliance': 'adherence',
    'perform': 'execute',
    'provide': 'furnish',
    'terminate': 'dissolve',
    'dispute resolution': 'conflict resolution',
    'intellectual property': 'proprietary rights',
    'marketing': 'promotion',
    'consulting': 'advisory services',
    'management': 'administration',
    'indemnification': 'compensation for harm or loss',
    'jurisdiction': 'legal authority',
    'clause': 'provision',
    'hereinafter': 'as referred hereafter',
    'whereas': 'considering that',
    'hereby': 'by this means',
    'undertake': 'commit to perform',
    'acknowledge': 'recognize formally',
    'agreement': 'accord',
    'contractor': 'contractual agent',
    'premises': 'property',
    'conflict': 'legal conflict',
    'litigation': 'legal proceedings',
    'settlement': 'amicable resolution',
    'appeal': 'judicial review',
    'testimony': 'legal testimony',
    'affidavit': 'sworn statement',
    'damages': 'compensatory payments',
    'liability': 'legal responsibility',
    'consent': 'formal agreement',
    'mutual': 'reciprocal',
    'terms and conditions': 'stipulated regulations',
    'provision': 'stipulation',
    'execution': 'enactment',
    'enforce': 'compel observance of',
    'abide by': 'comply with',
    'accordance': 'in conformity with',
    'pursuant to': 'in accordance with',
    'in witness whereof': 'in confirmation of which',
    'witness': 'observer of signing',
    'addendum': 'supplementary document',
    'annexure': 'attached document',
    'appendix': 'supplementary material',
    'arbitrator': 'mediator',
    'assent': 'approval',
    'assign': 'allocate',
    'binding': 'legally binding',
    'capacity': 'legal competence',
    'codicil': 'document amendment',
    'coerce': 'compel',
    'commence': 'begin',
    'concur': 'agree',
    'convey': 'transfer',
    'debtor': 'borrower',
    'decree': 'order',
    'defendant': 'accused',
    'demise': 'transfer by lease',
    'devise': 'bequeath',
    'disclose': 'reveal',
    'enactment': 'establishment through legal process',
    'endorse': 'approve',
    'entail': 'involve',
    'equity': 'fairness',
    'estoppel': 'prevention of denial',
    'ex gratia': 'as a favor',
    'fiscal': 'related to government revenue',
    'forbearance': 'refraining from enforcing',
    'foreclosure': 'termination of right to property',
    'herein': 'in this document',
    'incumbent': 'currently holding office',
    'injunction': 'judicial order',
    'insolvency': 'inability to pay debts',
    'instalment': 'partial payment',
    'insurer': 'underwriter',
    'irrevocable': 'not able to be changed',
    'lessee': 'tenant',
    'lessor': 'landlord',
    'lien': 'right to keep possession',
    'litigant': 'someone involved in a lawsuit',
    'litigate': 'take legal action',
    'mandate': 'official order',
    'moratorium': 'temporary prohibition',
    'negligence': 'failure to take proper care',
    'notary': 'official authorized to certify',
    'nullify': 'make legally null',
    'obligee': 'person to whom another is obligated',
    'obligor': 'person who is bound to another',
    'ordinance': 'a piece of legislation',
    'patent': 'government authority or license',
    'plaintiff': 'person who brings a case',
    'plead': 'make an emotional appeal',
    'proxy': 'authority to represent someone',
    'quasi': 'seemingly but not actually',
    'ratify': 'sign or give formal consent',
    'rebuttal': 'contradiction',
    'reciprocal': 'given, felt, or done in return',
    'recompense': 'compensation or reward',
    'redress': 'remedy or compensation',
    'relinquish': 'voluntarily cease to claim',
    'remand': 'place on bail or in custody',
    'remedy': 'means of legal reparation',
    'repeal': 'revoke or annul',
    'rescind': 'revoke, cancel, or repeal',
    'residue': 'remainder of estate',
    'resolution': 'a firm decision',
    'respondent': 'defendant in a lawsuit',
    'restitution': 'restoration of something lost',
    'retainer': 'a fee paid in advance',
    'revoke': 'put an end to validity',
    'sanction': 'penalty for disobeying',
    'subpoena': 'order to attend court',
    'sue': 'institute legal proceedings',
    'summons': 'order to appear before a judge',
    'testator': 'person who has made a will',
    'tort': 'wrongful act leading to legal liability',
    'transcript': 'written record of spoken events',
    'trustee': 'person given control or power of administration',
    'underwrite': 'sign and accept liability',
    'unilateral': 'performed by or affecting only one party',
    'verdict': 'decision on an issue',
    'vest': 'confer or bestow',
    'waive': 'refrain from insisting on',
    'writ': 'formal written order'
    }
    
    def get_legal_synonym(word):
        return legal_dictionary.get(word, word)

    tokens = word_tokenize(sentence.lower())
    tagged = pos_tag(tokens)
    transformed = [get_legal_synonym(word) for word, _ in tagged]
    return ' '.join(transformed).capitalize()

# Define processing functions
def extract_date(text):
    doc = nlp(text)
    date_entities = [ent for ent in doc.ents if ent.label_ == "DATE"]
    if date_entities:
        return date_entities[0].text
    return None

def format_date(date_text):
    dt = parse(date_text)
    return dt.strftime(f"{ordinal(dt.day)} %B %Y")

def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return str(n) + suffix

def validate_and_correct_name(text):
    doc = nlp(text)
    names = [ent for ent in doc.ents if ent.label_ == "PERSON"]
    if not names:
        return None, "No valid name found."
    
    full_name = names[0].text.split()
    if len(full_name) < 2:
        return None, "Please enter both first and last names."
    
    corrected_full_name = ' '.join(name.capitalize() for name in full_name)
    return corrected_full_name, ""

def process_amount(input_amount):
    stripped_amount = input_amount.replace(",", "")
    try:
        number = float(stripped_amount)
    except ValueError:
        return None, "The input is not a valid number."
    formatted_amount = "{:,.2f}".format(number)
    return formatted_amount, ""

def validate_days(input_days):
    try:
        days = int(input_days)
        if days < 1 or days > 31:
            return None, "The number of days must be between 1 and 31."
        return days, ""
    except ValueError:
        return None, "The input must be a numerical value."

def validate_and_format_address(address):
    patterns = {
        'house_no': re.compile(r'( s\sno\.?|flat\sno\.?|hno\.?|apartment|suite|unit|#\d+)', re.IGNORECASE),
        'street': re.compile(r'(street|st\.?|sector|road|rd\.?|lane|ln\.?|drive|dr\.?|boulevard|blvd\.?|avenue|ave\.?)', re.IGNORECASE),
        'city': re.compile(r'(city|town|village)', re.IGNORECASE),
        'state': re.compile(r'(state|province|region|county)', re.IGNORECASE),
        'country': re.compile(r'(country|nation)', re.IGNORECASE),
        'pin_code': re.compile(r'(postal\scode|postcode|zipcode|zip\scode|P\.?\s?O\.?\s?Box\s?\d+)', re.IGNORECASE)
    }
    components = {'house_no': False, 'street': False, 'city': False, 'state': False, 'country': False, 'pin_code': False}
    address_parts = re.split(r',\s*', address)
    for part in address_parts:
        for key, pattern in patterns.items():
            if pattern.search(part):
                components[key] = True
    missing_components = [key for key, found in components.items() if not found]
    if missing_components:
        return None, "Missing components: " + ", ".join(missing_components)
    formatted_address = ', '.join(part.strip() for part in address_parts if part)
    return formatted_address, ""

# Placeholder definitions
# placeholders = {

#             "\\textbf{\\textless{} Effective Date\\textgreater,}": "Enter the effective date of the agreement (e.g., 2024-04-26): ",
#         "\\textbf{\\textless{} Consultant\\textquotesingle s Name\\textgreater{}}": "Enter the name of the consultant: ",
#         "\\textless{} \\textbf{Client\\textquotesingle s Name}\\textgreater": "Enter the name of the client: ",
#         "\\textless{}\\textbf{Consultant's Address}\\textgreater": "Enter the consultant's address: ",
#         "\\textless{}\\textbf{Client's Address}\\textgreater{}": "Enter the client's address: ",
#         "\\textless{}\\textbf{Retainer Fee}\\textgreater{}": "Enter the retainer fee amount: ",
#         "\\textless{}\\textbf{Number of days}\\textgreater": "Enter the number of days within which the client must pay the invoice: ",
#         "\\textless{} \\textbf{Payment Method} \\textgreater{}": "Enter the payment method (e.g., bank transfer, check): ",
#         "\\textless{}\\textbf{Address}\\textgreater{}": "Enter the address where the payment should be sent: ",
#         "\\textless{}\\textbf{Expense Pre-Approval Threshold Amount}\\textgreater": "Enter the expense pre-approval threshold amount: ",
#         "\\textless{}\\textbf{Term End Date} \\textgreater": "Enter the end date of the term of the agreement: ",
#         "\\textless{}\\textbf{Notice Period for Termination Days\\textgreater{}}": "Enter the number of days notice required for termination: ",
#         "\\textless{}\\textbf{Arbitration/mediation/negotiation}\\textgreater{}": "Enter the method for dispute resolution (e.g., arbitration, mediation): ",
#         "\\textless{} \\textbf{Governing Law} \\textgreater": "Enter the governing law (e.g., the state or country): ",
#         "\\textless{}\\textbf{Client's Signature}\\textgreater{}": "Enter the placeholder for the client's signature: ",
#         "\\textless{}\\textbf{Consultant's Signature}\\textgreater{}": "Enter the placeholder for the consultant's signature: ",
#         "\\textless{}\\textbf{Date}\\textgreater{}": "Enter the date of signing: "
# }

# Function to process input based on its placeholder
def process_input(input_text, placeholder):
    if "Date" in placeholder:
        date = extract_date(input_text)
        if date:
            return format_date(date), ""
        else:
            return None, "Invalid date format."
    elif "Name" in placeholder:
        return validate_and_correct_name(input_text)
    elif "Fee" in placeholder:
        return process_amount(input_text)
    elif "Amount" in placeholder:
        return process_amount(input_text)
    elif "days" in placeholder:
        return validate_days(input_text)
    elif "Address" in placeholder:
        return validate_and_format_address(input_text)
    else:
        return input_text, ""  # For any input that does not need specific processing

# Streamlit app setup
# def main():
#     st.title('Document Processor')
#     responses = {}
#     errors = {}

#     for placeholder, description in placeholders.items():
#         user_input = st.text_input(description, key=placeholder)
#         if user_input:
#             processed_input, error = process_input(user_input, placeholder)
#             if error:
#                 st.error(f"Error for {description}: {error}")
#             else:
#                 responses[placeholder] = processed_input
#                 st.write(f"Processed for {description}: {processed_input}")

#     if st.button('Finalize Document') and all(responses.values()):
#         update_document('/path/to/your/template.tex', responses)
#         st.success("Document updated successfully!")

# if __name__ == "__main__":
#     main()


import subprocess
import os

def update_document(file_path, responses):
    # Read the original LaTeX file and update its content with responses
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    for placeholder, processed_input in responses.items():
        content = content.replace(placeholder, processed_input)  # Replace placeholder with user input

    # Define the path for the temporary updated LaTeX file
    temp_file_path = file_path.replace('.latex', '_temp.latex')

    # Write the modified content to a temporary LaTeX file
    with open(temp_file_path, 'w', encoding='utf-8') as file:
        file.write(content)

    # Convert the updated LaTeX file to PDF
    output_dir = os.path.dirname(temp_file_path)
    pdf_path = convert_file_to_pdf(temp_file_path, output_dir)

    # Clean up temporary LaTeX file
    os.remove(temp_file_path)

    # Inform the user of the successful conversion
    st.success(f"Updated document saved as PDF at {pdf_path}")

    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="Download Updated Document",
                data=pdf_file,
                file_name=os.path.basename(pdf_path),
                mime='application/pdf'
            )


 
            
    return pdf_path

def convert_file_to_pdf(file_path, output_dir='./'):
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    command = ['/Library/TeX/texbin/pdflatex', '-output-directory', output_dir, file_path]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Clean up auxiliary files generated by LaTeX
    aux_files_extensions = ['.aux', '.log', '.out']
    for ext in aux_files_extensions:
        try:
            os.remove(os.path.join(output_dir, f"{base_name}{ext}"))
        except OSError:
            pass

    return os.path.join(output_dir, f"{base_name}.pdf")



def main():
    st.title('Document Processor')
    responses = {}
    errors = {}
    col1, col2 = st.columns([3, 1])


    with col1:
    
        # Add your placeholders here
        placeholders = {

            "\\textless{}\\textbf{Effective Date}\\textgreater{}": "Enter the effective date of the agreement (e.g., 2024-04-26): ",
            "\\textless{}\\textbf{Clients Name}\\textgreater{}": "Enter the Client's name: ", #updated
            # "\\textless{}\\textbf{Client\\textquotesingle s Name}\\textgreater{}": "Enter the Client's name: ",
            "\\textless{}\\textbf{Clients Address}\\textgreater": "Enter the Client's address", #updated
            # "\\textless{}\\textbf{Client\\textquotesingle s Address}\\textgreater": "Enter the Client's address",
            "\\textless{}\\textbf{Marketers Name}\\textgreater{}": "Enter the Marketer's name: ", #updated
            # "\\textless{}\\textbf{Marketer\\textquotesingle s Name}\\textgreater{}": "Enter the Marketer's name: ",
            "\\textless{}\\textbf{Marketers Address}\\textgreater{}": "Enter the Marketer's address", #updated
            # "\\textless{}\\textbf{Marketer\\textquotesingle s Address}\\textgreater{}": "Enter the Marketer's address",
            "\\textless{}\\textbf{Completion Date}\\textgreater": "Enter the Completion date: ",
            "\\textless{}\\textbf{Total Cost}\\textgreater": "Enter the Total cost: ",
            "\\textless{}\\textbf{Percentage or Cost}\\textgreater{}": "Enter the Percentage or Cost to be to be paid at the signing of this agreement: ", #updated
            # "\\textless{}\\textbf{Percentage or Cost}\\textgreater{}": "Enter the Percentage or Amount to be to be paid at the signing of this agreement: ",
            "\\textless{}\\textbf{Percentage or Amount}\\textgreater{}": "Enter the Percentage or Amount to be to be paid at the completion of this agreement: ",
            "\\textless Frequency\\textgreater{}": "Enter the frequency of days: ",
            "\\textless{}\\textbf{Threshold Amount}\\textgreater": "Enter the Threshold Amount: ", #updated
            # "\textless{}\textbf{Threshold Amount}\textgreater": "Enter the Threshold Amount: ",
            "\\textless{}\\textbf{Payment Method}\\textgreater": "Enter the payment method: ",
            "\\textless{}\\textbf{End Date\\textgreater": "Enter the end date",
            "\\textbf{\\textless Time Period\\textgreater.}": "Enter the time period", #updated
            # "\\textbf{\\textless Time Period\\textgreater.}": "Enter the time period",
            "\\textbf{\\textless Number of Days\\textgreater{}}": "Enter the number of days: ", #updated
            # "\\textbf{\\textless Number of Days\\textgreater{}}": "Enter the number of days: ",
            "\\textless{}\\textbf{Arbitration/mediation/negotiation}\\textgreater{}": "Enter the method for dispute resolution (e.g., arbitration, mediation):",
            "\\textbf{\\textless{} Jurisdiction\\textgreater.}": "Enter the Jurisdiction",
            "\\textless{}\\textbf{Marketer\\textquotesingle s Name\\textgreater{}}": "Enter the Marketer's name: ",
            "\\textbf{\\textless Marketer\\textquotesingle s Signature\\textgreater{}}": "Marketer's Signature: ",
            "\\textless Client\\textquotesingle s Name\\textgreater{}": "Enter the Client's Name:",
            "\\textbf{\\textless Client\\textquotesingle s Signature\\textgreater{}}": "Client's Signature",
            "\\textbf{\\textless Date\\textgreater{}}": "Enter Date: "
        }
            
        

        for placeholder, description in placeholders.items():
            user_input = st.text_input(description, key=placeholder)
            if user_input:
                processed_input, error = process_input(user_input, placeholder)
                if error:
                    st.error(f"Error for {description}: {error}")
                else:
                    responses[placeholder] = processed_input
                    st.write(f"Processed for {description}: {processed_input}")

        additional_clause = st.text_area("Enter any additional clause:", key="additional_clause")
        if additional_clause:
            corrected_clause = correct_text(additional_clause)
            transformed_clause = transform_sentence(corrected_clause)
            #passive_clause = active_to_passive(transformed_clause)  # Convert to passive voice
            st.write("Corrected, Transformed, and Passive Clause:", transformed_clause)


        uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
        uploaded_file2 = None  # Define uploaded_file2 here

        # if uploaded_file:
        #     #uploaded_file2 = process_pdf_signature(uploaded_file)  
        #     #st.write("Uploaded File 2:", uploaded_file2)
        #     uploaded_file2 = "/Users/riditjain/Desktop/output.png" 
        #     if uploaded_file2:
        #         content = uploaded_file2.read()  
        #         st.write(content.decode())

        if uploaded_file:
            uploaded_file2 = "/Users/akshatmanohar/Downloads/IMG_1266.png"  # Path to your image
        if uploaded_file2:
            st.image(uploaded_file2, caption='Uploaded Image') 



    

        if st.button('Finalize Document') and all(responses.values()):
            update_document('/Users/akshatmanohar/Downloads/Nlp latex/vertopal.com_Marketing-Agreement-Template-Signaturely.latex', responses)
            st.success("Document updated successfully!")
    
    # with col2:  # PDF viewer on the right
    #     pdf_path = "/Users/riditjain/Desktop/crypto q3.pdf"  # Specify the path to the PDF file here
    #     st.write("PDF File:")
    #     with open(pdf_path, "rb") as pdf_file:
    #         st.download_button(label="Download PDF", data=pdf_file, file_name="Your_Document.pdf", mime="application/pdf")

    with col2:  # PDF viewer on the right
    #     pdf_path = "/Users/riditjain/Desktop/crypto q3.pdf"  # Specify the path to the PDF file here
    #     with open(pdf_path, "rb") as pdf_file:
    #         base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
    #     pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    #     st.markdown(pdf_display, unsafe_allow_html=True)

        pdf_path = "/Users/akshatmanohar/Desktop/ACFrOgBm8pOXyunH-OWPVH5OYkrMQ60Got5B4xesvy-7g0QPFxXzLjki8tiImqlCWyn802P4BtHIpIrL7_6TK28U_H0JS0IhCPH0fwHbk15U03wrU8OlWECr9jPMCOMVZ-3cXSWvv-QMdgvyzlXCEQOC5a6w--0XWq3tRuyYZg==.pdf"  # Specify the path to the PDF file here
        with open(pdf_path, "rb") as pdf_file:
            base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
        
        # Embed PDF without toolbar and with a default zoom
        pdf_display = f'''
        <embed src="data:application/pdf;base64,{base64_pdf}#toolbar=0&zoom=100" 
            type="application/pdf" 
            width="700" 
            height="1000"
            style="overflow:auto;resize:none;"
            sandbox="allow-scripts allow-same-origin">
        '''
        st.markdown(pdf_display, unsafe_allow_html=True)





if __name__ == "__main__":
    main()
