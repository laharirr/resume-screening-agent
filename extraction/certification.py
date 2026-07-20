CERTIFICATIONS = [
    "AWS",
    "Azure",
    "Google Cloud",
    "TensorFlow",
    "Oracle",
    "Microsoft",
    "Cisco",
    "Red Hat",
    "Coursera",
    "Udemy"
]


def extract_certifications(text):

    found = []

    lower = text.lower()

    for cert in CERTIFICATIONS:

        if cert.lower() in lower:
            found.append(cert)

    return found