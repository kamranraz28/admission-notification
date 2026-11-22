"""
Universities to monitor.

Add or remove entries here. Each entry needs:
    id               : a short unique name used in notified.json
    name             : the name shown in Telegram
    urls             : official notice page(s) and/or admission portal(s)
    needs_javascript : optional; set True for JavaScript-heavy portals

Tips:
    - Prefer the admission notice page and the online application portal.
    - URLs are checked in order. Links found on these pages that look
      admission-related are also followed (up to MAX_PAGES_PER_UNIVERSITY).
    - Use the official university domain. The bot does not use Google search.
    - "needs_javascript" only works when Playwright is installed.
"""

UNIVERSITIES = [
    {
        "id": "ju",
        "name": "Jahangirnagar University",
        "urls": [
            "https://juadmission.org/application-instruction",
            "https://juadmission.org/",
            "https://juniv.edu/",
        ],
    },
    {
        "id": "bup",
        "name": "Bangladesh University of Professionals (BUP)",
        "urls": [
            "https://admission.bup.edu.bd/admission/Home",
            "https://bup.edu.bd/",
        ],
    },
    {
        "id": "cu",
        "name": "University of Chittagong",
        "urls": [
            "https://cu.ac.bd/notice-board/",
            "https://admission.cu.ac.bd/admission-circular",
        ],
    },
    {
        "id": "ru",
        "name": "University of Rajshahi",
        "urls": [
            "https://ru.ac.bd/admission",
            "https://admission.ru.ac.bd/",
        ],
    },
    {
        "id": "ku",
        "name": "Khulna University",
        "urls": [
            "https://ku.ac.bd/notices",
            "https://admission.ku.ac.bd/",
        ],
    },
    {
        "id": "cou",
        "name": "Comilla University",
        "urls": [
            "https://cou.ac.bd/q/admission",
            "https://cou.ac.bd/",
        ],
    },
    {
        "id": "gst",
        "name": "GST / Guccho Integrated Admission",
        "urls": [
            "https://gstadmission.ac.bd/",
        ],
        "needs_javascript": True,
    },
]
