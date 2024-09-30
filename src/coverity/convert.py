import xml.etree.ElementTree as ET
import os
import sys
 
model_interface_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model_interface'))
sys.path.insert(0, model_interface_path)
from ollama_interface import codeReview_ollama
 
prompt_dict = {}
 
def print_file_details(xml_path, output_path):
    # Check if the XML file exists
    if not os.path.isfile(xml_path):
        with open(output_path, 'w') as f:
            f.write(f"Error: The file at {xml_path} does not exist.\n")
        return
   
    try:
        # Load and parse the XML file
        tree = ET.parse(xml_path)
        root = tree.getroot()
 
        # Open the output file for writing
        with open(output_path, 'w') as f:
            # Print root tag to confirm successful parsing
            f.write(f"Root tag: {root.tag}\n")
           
            # Iterate over each 'error' element
            found_any_file = False
            for error in root.findall('error'):
                found_any_file = True
                checker = error.find('checker').text if error.find('checker') is not None else 'N/A'
                file_name = error.find('file').text if error.find('file') is not None else 'N/A'
                function = error.find('function').text if error.find('function') is not None else 'N/A'
               
                if not("src/database/bcmdnxwr.c" in file_name and function == "NpWrFsMplsHwVpwsCreatePwVc"):
                    continue
               
                if file_name not in prompt_dict:
                    prompt_dict[file_name] = {}
                if function not in prompt_dict[file_name]:
                    prompt_dict[file_name][function] = []
 
                for event in error.findall('event'):
                    # Extract information from each event element
                    name = event.find('name').text if event.find('name') is not None else 'N/A'
                    line = event.find('line').text if event.find('line') is not None else 'N/A'                
                    description = event.find('description').text if event.find('description') is not None else 'N/A'
 
                    # Write the details to the file
                    f.write(f'Error_type: {checker}\n')
                    f.write(f'File Name: {file_name}\n')
                    f.write(f'Line Number: {line}\n')
                    f.write(f'Function Name: {function}\n')
                    f.write(f'Description (coverity tool output): {description}\n')
                    f.write('---\n')
                   
                   
                    #adjusted_line = int(line) + 33015
                    #adjusted_line = int(line) + 33015 if line.isdigit() else 'N/A'
                    prompt_dict[file_name][function].append(f"Issue has been found on {line} and this is the description for the same: {description}")
 
            if not found_any_file:
                f.write("No 'file' elements found in the XML.\n")
   
    except ET.ParseError as e:
        with open(output_path, 'w') as f:
            f.write(f"Error parsing XML: {e}\n")
    except Exception as e:
        with open(output_path, 'w') as f:
            f.write(f"An error occurred: {e}\n")
 
# Specify the path to the XML file and the output file
xml_file_path = r'C:\Users\vaishaja\github_codereview\ToT\code_review_app\src\coverity\CHECKED_RETURN.errors.xml'
output_file_path = r'C:\Users\vaishaja\github_codereview\ToT\code_review_app\src\coverity\output.txt'
 
print_file_details(xml_file_path, output_file_path)
 
def code_review_prompt2():
    prompt = '''
Example ::
 
1."Below is the Coverity output error".
 
Description (coverity tool output): {CovLStrv2{{t{Condition {0}, taking true branch.}{{code{pMplsVrfMapInfo->u4RefCount == 0}}}}}}
 
2. "This is the base code in which the error identified by Coverity has been detected."
 
if (pMplsVrfMapInfo->u4RefCount == 0)
        {
            bcm_l3_egress_destroy (i4UnitId, pMplsVrfMapInfo->EgrObjId);
            bcm_mpls_tunnel_initiator_clear (i4UnitId,
                    pMplsVrfMapInfo->TunnelId);
        }
 
3. "This is the corrected code that addresses those errors."
 
if (pMplsVrfMapInfo->u4RefCount == 0)
         {
            bcm_l3_egress_destroy (i4UnitId, pMplsVrfMapInfo->EgrObjId);
            i4RetChk = bcm_l3_egress_destroy (i4UnitId, pMplsVrfMapInfo->EgrObjId);
            if (i4RetChk != BCM_E_NONE)
            {
                NP_DEBUG_TRC (CLI_ISS_NP_LOG_ERROR_LEVEL, NPAPI_BCMX,
                                    "ERROR [NP] bcm_l3_egress_destroy failed\r\n");
            }
             bcm_mpls_tunnel_initiator_clear (i4UnitId,
                     pMplsVrfMapInfo->TunnelId);
         }
Above, I have provided the base code that contains errors, as well as the corrected code that addresses those errors. Please use this code snippet as a reference and provide the output accordingly.
 
I need your assistance in analyzing a C function from a code file that begins at line number 33016. Below are the points to consider based on the static analysis results:
 
1 . Identify the Errors: For each error detected by the static analysis application, specify the type of error, including the line number where it was found.
2 . Base Code: Give the original code snippet from which the error was identified.
3 . Corrected Code: Provide the corrected code generated by CodeLlama that addresses each identified issue.
Additionally, please ensure that the corrections adhere to best practices in C programming. If applicable, suggest any additional checks or improvements to enhance the robustness and maintainability of the code.
 
Here are the details extracted from the error reports:
 
'''
   
    for file_name in prompt_dict:
        for function, val in prompt_dict[file_name].items():
            prompt += f"Function name is: {function}\n"
            prompt += "\n".join(val[:5]) + "\n"
    return prompt
 
file_path =  r'C:\Users\vaishaja\github_codereview\ToT\code_review_app\src\coverity\bcmdnxwr.c'
 
file_name = os.path.basename(file_path)
print(f"Processing file: {file_name}")
   
# Open and read the file
with open(file_path, 'r') as file:
    file_content = file.read()
   
prompt = code_review_prompt2()
print("{0}\n{1}".format(file_content, prompt))
comments = codeReview_ollama(code=file_content, prompt=code_review_prompt2())
print(comments)