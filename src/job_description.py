def get_job_description() -> str:
    print("\nPaste the job description below.")
    print("When finished, enter a blank line.")

    lines = []

    try:
        while True:
            line = input()
            if not line.strip():
                break
            lines.append(line)
    
    except EOFError as error:
        raise ValueError("Job description input was interrupted. Please try again.") from error

    job_description = "\n".join(lines).strip()

    if not job_description:
        raise ValueError("Job description cannot be empty.")

    return job_description
    