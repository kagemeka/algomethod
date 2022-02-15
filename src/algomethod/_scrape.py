import bs4


def _parse_html(html: str) -> bs4.BeautifulSoup:
    return bs4.BeautifulSoup(html, "html.parser")
