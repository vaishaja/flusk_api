def code_review_prompt():
    prompt = '''
    Please evaluate the above code with the following additional context. Above code is a patch of pull request. Evaluate the changes only and provide suggestions as suggested in below contexts:

    Use the following checklist to guide your analysis:

    1. Documentation Defects:
        a. Naming: Assess the quality of software element names.
        b. Comment: Analyze the quality and accuracy of code comments.

    2. Visual Representation Defects:
        a. Bracket Usage: Identify any issues with incorrect or missing brackets.
        b. Indentation: Check for incorrect indentation that affects readability.
        c. Long Line: Point out any long code statements that hinder readability.

    3. Structure Defects:
        a. Dead Code: Find any code statements that serve no meaningful purpose.
        b. Duplication: Identify duplicate code statements that can be refactored.

    4. New Functionality:
        a. Use Standard Method: Determine if a standardized approach should be used for single-purpose code statements.

    5. Resource Defects:
        a. Variable Initialization: Identify variables that are uninitialized or incorrectly initialized.
        b. Memory Management: Evaluate the program's memory usage and management.

    6. Check Defects:
        a. Check User Input: Analyze the validity of user input and its handling.

    7. Interface Defects:
        a. Parameter: Detect incorrect or missing parameters when calling functions or libraries.

    8. Logic Defects:
        a. Compute: Identify incorrect logic during system execution.
        b. Performance: Evaluate the efficiency of the algorithm used.

    9. Identify any errors or code improvements in the provided line of code.
    10. Specify the line number where the error or code improvements occur.
    11. Provide a corrected version of the code if an error is detected.
    

    Provide your feedback in a numbered list for each category. 
    At the end of your answer, summarize the recommended changes to improve the quality of the code provided.
    Also, provide corrected source code with your comments incorporated.
    '''
    return prompt
