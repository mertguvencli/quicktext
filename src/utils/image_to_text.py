try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import platform


class ImageToText:
    exec_path = {
        "Darwin": "/usr/local/Cellar/tesseract/4.1.1/bin/tesseract",
        "Linux": "/usr/bin/tesseract",
    }
    timeout = 30

    pytesseract.pytesseract.tesseract_cmd = exec_path.get(
        platform.system()
    )

    def __init__(self, path: str, lang="eng") -> None:
        self.path = path
        self.lang = lang

    def convert(self) -> str:
        response = None
        try:
            response = pytesseract.image_to_string(
                image=Image.open(self.path),
                lang=self.lang,
                timeout=self.timeout
            )
            return response
        except:  # noqa
            response = "We could not convert to text:("
            return response
