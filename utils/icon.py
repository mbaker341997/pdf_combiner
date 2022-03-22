import base64


# encoded version of pdf_icon.gif. why do it this way? to make pyinstaller play nice
def get_pdf_icon():
    icon_base64 = """
    R0lGODlhEAAQAHAAACH5BAEAAAQALAAAAAAQABAAggAAAAA///8ADH8A/wAAAAAAAAAAAAAAAAM
    wSLrcTiHK8NSUFV7ahB/ggHVfODKeEIqRk67n8potqdIcWoKxkv6ZXyooFGSOyEoCADs=
    """
    return base64.b64decode(icon_base64)
