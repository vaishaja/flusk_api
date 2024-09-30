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

def code_review_prompt_static_analysis():

    prompt = '''

    "Please analyze the provided code for potential issues and present your findings in a clear and structured format. Organize the issues into sections with concise headings and detailed descriptions. For each issue, include the following:

    1. Issue Description: A brief explanation of the problem.
    2. Line Number: The specific line number where the issue occurs.
    3. Proposed Solution: Recommendations a code on how to fix the issue.
    Make sure to format the response with bullet points or numbered lists to enhance readability. Here’s the code for analysis:

Review Aspects

    Security Vulnerabilities:
    1.Identify issues like buffer overflows, SQL injection, and cross-site scripting.
    2.Suggest mitigation strategies.

    Memory Management Issues:
    1.Look for memory leaks and null pointer dereferences.
    2.Recommend improvements to prevent these issues.

    Concurrency Problems:
    1.Check for race conditions and deadlocks.
    2.Provide solutions for ensuring thread safety.

    Performance Optimization:
    1.Assess for inefficient algorithms and unnecessary loops.
    2.Suggest specific performance enhancements.

    Compliance with Coding Standards:
    1.Evaluate adherence to standards like MISRA C or CERT C.
    2.Identify non-compliance and suggest corrections.

    Proper Resource Management:
    1.Review management of resources (file handles, network connections).
    2.Identify leaks and recommend better handling.

    Logical Errors and Edge Cases:
    1.Identify logical errors and unhandled edge cases.
    2.Recommend robust handling strategies.

    Robustness in Error Handling:
    1.Evaluate the effectiveness of error handling.
    2.Suggest improvements for fault tolerance.

    Code Complexity and Maintainability:
    1.Assess cyclomatic complexity and readability.
    2.Identify areas for simplification and refactoring.

    Adherence to Security Best Practices:
    1.Check for security best practices like encryption and secure protocols.

    Recommend improvements.
    Conduct a comprehensive review of the code covering all the above aspects, identifying specific issues and providing actionable suggestions. '''