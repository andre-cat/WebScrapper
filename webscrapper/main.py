from pages import exhibitorlist


def main() -> None:

    try:
        print("WEBSCRAPPER")
        # exhibitorlist.scrap(1, 737)
        exhibitorlist.translate()
    except Exception as e:
        print(f"FATAL EXCEPTION: {e}")
