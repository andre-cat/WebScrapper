import time
from typing import cast

from webscrapper.browser import Browser, WebElement
from webscrapper.excel import Excel, Worksheet
from webscrapper.scrapper import Content, ResultSet, Scrapper, Tag
from webscrapper.translator import Translator
from webscrapper.utils import Files, Timer

file_name: str = "exhibitorlist"


def scrap(page_start: int = 1, page_end: int = 737) -> None:

    def get_sheet_number(page: int) -> int:
        return 0 if page < 100 else page // 100

    def get_row(record_number: int, sheet_number: int) -> int:
        index: int = record_number

        if record_number <= 99:
            index = record_number + 1
        else:
            index -= (12 * 99) + (12 * 100 * (sheet_number - 1)) - 1

        return index

    def get_sheet(excel: Excel, name: str) -> Worksheet:
        if not excel.has_sheet(name):
            excel.create_sheet(name)

        sheet: Worksheet = excel.get_sheet(name)

        sheet["A1"] = "done"
        sheet["B1"] = "page"
        sheet["C1"] = "number"
        sheet["D1"] = "text"
        sheet["E1"] = "images"
        sheet["F1"] = "videos"
        sheet["G1"] = "links"
        sheet["H1"] = "company"
        sheet["I1"] = "address"
        sheet["J1"] = "website"
        sheet["K1"] = "logo"
        sheet["L1"] = "url"
        sheet["M1"] = "error"

        return sheet

    def go_to_page(browser: Browser, page: int = 0) -> int | None:
        success: bool = False
        attempts: int = 0

        while not success and attempts < 3:
            button_number: int = 0

            try:
                browser.wait_css_clickable(".layui-laypage-next")

                next_button: WebElement | None = browser.find_one_by_css(".layui-laypage-next")

                if next_button:
                    if page > 0:
                        browser.set_attribute(next_button, "data-page", str(page))
                    button_number = int(next_button.get_attribute("data-page") or "0")
                    print(f"Going to page {button_number}")
                    browser.click_element(next_button)
                    success = True
            except Exception as e:
                attempts += 1
                print(f"Error going to page: {e}")
                time.sleep(5)

        if success:
            return button_number
        else:
            raise Exception(f"It was not possible to go to the page {page}")

    print(file_name)
    print(f"Scrapping pages from {page_start} to {page_end}")

    excel: Excel = Excel(file_name)
    Files.copy_file(f"{file_name}.xlsx", f"{file_name}_backup.xlsx")

    sheet_number: int = get_sheet_number(page_start)
    sheet: Worksheet = get_sheet(excel, str(sheet_number))

    browser: Browser = Browser()
    browser.go_to_url("https://www.cmef.com.cn/exhibitorlist?type=1", 5)

    page: int = go_to_page(browser, page_start) or 1

    record_number: int = (page - 1) * 12
    row: int = get_row(record_number, sheet_number)

    error_number: int = 0

    while error_number < 5:
        print(f"{'_' * 5} Page {page} {'_' * 5}")

        browser.wait_css_present(".exc-item.clearfix")
        browser.wait_css_present(".exc-item-title.inner")

        scrapper: Scrapper = Scrapper(browser.get_page_source_code())

        scrapper.delete_tags("head")

        items_parent: Tag | None = scrapper.find_one("div", "exl-r")

        if items_parent:
            scrapper.set_root(items_parent)

            items: ResultSet[Tag] | None = items_parent.find_all("div", class_=["company-item"])

            if not items:
                raise Exception("Cards not found")
            else:
                for item_index in range(len(items)):

                    timer = Timer()
                    timer.start_timer()

                    record_number += 1
                    row += 1

                    print(f"{'=' * 3} Record {record_number} | Item {item_index + 1} {'=' * 3}")

                    is_done: bool = sheet[f"A{row}"].value == "YES"

                    if is_done:
                        print("Already browsed")
                    else:

                        item: Tag = items[item_index]

                        done: str = "YES"
                        text: str = "\u274C"
                        images: str = "\u274C"
                        videos: str = "\u274C"
                        links: str = "\u274C"
                        company: str = "\u274C"
                        address: str = "\u274C"
                        website: str = "\u274C"
                        logo: str = "\u274C"
                        url: str = "\u274C"
                        error: str = '=""'

                        success: bool = False
                        attempts: int = 0

                        while not success and attempts < 3:
                            print(f"< Attempt {attempts + 1} >")

                            try:
                                # title_element: PageElement | None = card.find("div", class_=["exc-item-title"], title=True)
                                # title = title_element.text if title_element else ""

                                # if not title:
                                #     title = "\u274C"
                                #     raise Exception("Title not found")

                                url_element: Tag | None = item.div or None
                                unprocessed_url: list[str] | str = url_element["data-href"] if url_element else ""
                                url = unprocessed_url if isinstance(unprocessed_url, str) else "".join(unprocessed_url)

                                if not url:
                                    raise Exception("URL attribute not found")
                                else:
                                    url = f"https://www.cmef.com.cn/{url}"

                                    browser.open_tab(url)
                                    browser.go_to_tab(2)

                                    # browser.wait_css_present(".company-header>.img")
                                    # browser.wait_css_present(".title-container>h2")
                                    # browser.wait_css_present(".address")
                                    # browser.wait_css_present(".website")
                                    browser.wait_css_present(".company-detail")

                                    browser.delete_scripts()

                                    second_scrapper: Scrapper = Scrapper(browser.get_page_source_code())

                                    second_scrapper.delete_tags("head")

                                    company_detail: Tag | None = second_scrapper.find_one("div", "company-detail")

                                    if not company_detail:
                                        raise Exception("Company detail not found")
                                    else:
                                        second_scrapper.set_root(company_detail)

                                        section_element: Tag | None = second_scrapper.find_one("div", "section")

                                        if not section_element:
                                            raise Exception("Section content not found")
                                        else:

                                            content_element: Tag | None = cast(Tag, section_element.find("div", "comp-detail"))

                                            if not content_element:
                                                raise Exception("Content not found")
                                            else:
                                                content: Content = second_scrapper.get_content(content_element)

                                                text = content.text
                                                images = content.images
                                                videos = content.videos
                                                links = content.links

                                        company_header: Tag | None = second_scrapper.find_one("div", ["company-header"])

                                        if not company_header:
                                            raise Exception("Company element not found")
                                        else:

                                            title_container: Tag | None = cast(Tag, company_header.find("div", class_="title-container"))

                                            if title_container:
                                                name_element: Tag | None = title_container.h2 if title_container else None
                                                company = name_element.text if name_element else ""

                                                if not company:
                                                    raise Exception("Name not found")

                                                address_element_parent: Tag | None = cast(Tag, title_container.find("p", class_="address"))
                                                address_element: Tag | None = address_element_parent.span if address_element_parent else None
                                                address = address_element.text if address_element else ""

                                                website_element_parent: Tag | None = cast(Tag, title_container.find("p", class_="website"))
                                                website_element: Tag | None = website_element_parent.a if website_element_parent else None
                                                website = website_element.text if website_element else ""

                                            logo_element: Tag | None = cast(Tag, company_header.find("img"))
                                            unprocessed_logo: list[str] | str = logo_element["src"] if logo_element else ""
                                            logo = unprocessed_logo if isinstance(unprocessed_logo, str) else "".join(unprocessed_logo)

                                    browser.close_tab()

                                success = True

                            except Exception as e:
                                error_number += 1

                                attempts += 1

                                done = "NO"
                                error = str(e)

                                print("❌ Error:", e)
                            finally:
                                sheet[f"A{row}"] = done
                                sheet[f"B{row}"] = page
                                sheet[f"C{row}"] = record_number
                                sheet[f"D{row}"] = text
                                sheet[f"E{row}"] = images
                                sheet[f"F{row}"] = videos
                                sheet[f"G{row}"] = links
                                sheet[f"H{row}"] = company
                                sheet[f"I{row}"] = address
                                sheet[f"J{row}"] = website
                                sheet[f"K{row}"] = logo
                                sheet[f"L{row}"] = url
                                sheet[f"M{row}"] = error

                                excel.save_book()
                                Files.copy_file(
                                    f"{file_name}.xlsx",
                                    f"{
                                                file_name}_copy.xlsx",
                                )

                    timer.stop_timer()

                    print(f"Seconds: {timer.get_elapsed_time():.2f}")

        if page_end > page:
            page = go_to_page(browser) or 1

            if page % 100 == 0:
                sheet_number = get_sheet_number(page)
                sheet = get_sheet(excel, str(sheet_number))
                row = get_row(record_number, sheet_number)
        else:
            break

    if error_number:
        print("Execution stopped due to errors")

    excel.close()
    browser.quit()


# def separate_content() -> None:
#     excel: Excel = Excel(file_name)
#     Files.copy_file(f"{file_name}.xlsx", f"{file_name}_backup.xlsx")

#     print(file_name)
#     print(
#         f"Separating content from {
#           excel.sheets[0].title} to {excel.sheets[-1].title}"
#     )

#     for sheet in excel.sheets:
#         print(f"{'=' * 5} Sheet {sheet.title} {'=' * 5}")

#         sheet["D1"] = "text"
#         sheet["E1"] = "images"
#         sheet["F1"] = "videos"
#         sheet["G1"] = "links"

#         for row in range(28, sheet.max_row + 1):

#             print(f"{'_' * 3} Row {row} {'_' * 3}")

#             is_content_separated: bool = (
#                 sheet[f"E{row}"].value != '=""'
#                 or sheet[
#                     f"F{
#                 row}"
#                 ].value
#                 != '=""'
#                 or sheet[f"G{row}"].value != '=""'
#             )

#             if is_content_separated:
#                 print("Content already separated")
#             else:
#                 content: str = sheet[f"D{row}"].value
#                 separated_content: Content = separate_content_cell(content)
#                 sheet[f"D{row}"] = separated_content.text or "\u2717"
#                 sheet[f"E{row}"] = separated_content.images or "\u2717"
#                 sheet[f"F{row}"] = separated_content.videos or "\u2717"
#                 sheet[f"G{row}"] = separated_content.links or "\u2717"

#                 excel.save_book()

#                 Files.copy_file(f"{file_name}.xlsx", f"{file_name}_copy.xlsx")

#     excel.close()


# def separate_content_cell(content: str) -> Content:
#     text: str = ""
#     images: str = ""
#     videos: str = ""
#     links: str = ""

#     remaining: str

#     images_separator: str = f"{'=' * 10} IMAGES {'=' * 10}"
#     videos_separator: str = f"{'=' * 10} VIDEOS {'=' * 10}"
#     links_separator: str = f"{'=' * 10} LINKS {'=' * 10}"

#     if images_separator in content:
#         text, remaining = content.split(images_separator, 1)
#         if videos_separator in remaining:
#             images, remaining = remaining.split(videos_separator, 1)
#             if links_separator in remaining:
#                 videos, links = remaining.split(links_separator, 1)
#             else:
#                 videos = remaining
#         else:
#             images = remaining
#     else:
#         text = content

#     text = text.replace("=" * 10, "").strip()
#     images = "IMAGES\n" + images.strip() if images else ""
#     videos = "VIDEOS\n" + videos.strip() if videos else ""
#     links = "LINKS\n" + links.strip() if links else ""

#     return Content(text, images, videos, links)


def translate() -> None:

    excel: Excel = Excel(file_name)
    Files.copy_file(f"{file_name}.xlsx", f"{file_name}_backup.xlsx")

    print(file_name)
    print(
        f"Translating sheets from {
          excel.sheets[0].title} to {excel.sheets[-1].title}"
    )

    translator: Translator = Translator("zh-CN", "es")

    for sheet in excel.sheets:
        print(f"{'=' * 5} Sheet {sheet.title} {'=' * 5}")

        sheet["N1"] = "translated"
        sheet["O1"] = "text_es"
        sheet["P1"] = "company_es"

        timer: Timer = Timer()

        for row in range(2, sheet.max_row + 1):

            timer.start_timer()

            print(f"{'_' * 3} Row {row} {'_' * 3}")

            is_translated: bool = sheet[f"N{row}"].value == "YES"

            if is_translated:
                print("Already translated")
            else:
                translated = "YES"
                text_translated: str = translator.translate(sheet[f"D{row}"].value)
                company_translated: str = translator.translate(sheet[f"H{row}"].value)

                sheet[f"N{row}"] = translated
                sheet[f"O{row}"] = text_translated
                sheet[f"P{row}"] = company_translated

                excel.save_book()

                Files.copy_file(f"{file_name}.xlsx", f"{file_name}_copy.xlsx")

            timer.stop_timer()

            print(f"Seconds: {timer.get_elapsed_time():.2f}")

    excel.close()
