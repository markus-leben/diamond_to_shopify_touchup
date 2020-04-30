import csv
import os
import json

with open("config.json") as config_file:
    CONFIG = json.load(config_file)


def debug_print(debug_lvl, req_lvl, print_str):
    if debug_lvl >= req_lvl:
        print(print_str)


def recurcive_file_list(dir_name):
    list_of_file = os.listdir(dir_name)
    all_files = []
    for file in list_of_file:
        if file in ["venv",".idea"]:  # directories no ordinary person would be messing with
            continue
        full_path = os.path.join(dir_name, file)
        if os.path.isdir(full_path):
            all_files = all_files + recurcive_file_list(full_path)
        else:
            all_files.append(full_path)

    return all_files


def touch_up_csvs(bugging=0):
    debug_print(bugging, 1, "loading directory path: %s" % os.getcwd())
    array_to_save = []
    for filename in recurcive_file_list(os.getcwd()):
        debug_print(bugging, 1, "checking file: %s" % filename)
        if "ShopifyImportFile" in filename and ".csv" in filename:
            debug_print(bugging, 1, " shopify file found, beginning edit...")
            with open(filename, encoding="utf8") as raw_file:
                reader = csv.reader(raw_file, delimiter=",")
                line = 1 # counting from 1 because excel and openoffice count lines from 1
                for i in reader:
                    if line != 1:
                        debug_print(bugging, 1, "  editing line %s: %s" % (line, i))

                        debug_print(bugging, 1, "   editing title: %s" % i[1])
                        i[1] = i[1].title()
                        for j in CONFIG["title_rep_dict"]:
                            if j in i[1]:
                                i[1] = i[1].replace(j, CONFIG["title_rep_dict"][j])

                        while '(' in i[1]:
                            starter = i[1].find('(')
                            ender = i[1][starter:].find(')')

                            if ender != -1:
                                i[1] = i[1].replace(i[1][starter:ender+starter+1], '')
                            else:
                                i[1] = i[1].replace(i[1][starter:], '')
                            i[1] = i[1].strip()

                        debug_print(bugging, 1, "   title after editing: %s" % i[1])

                        debug_print(bugging, 1, "   editing vendor: %s" % i[3])
                        i[3] = i[3].title()
                        i[3] = i[3].replace('Dc', 'DC')
                        i[3] = i[3].strip()
                        debug_print(bugging, 1, "   vendor after editing: %s" % i[3])

                        debug_print(bugging, 1, "   adding vendor to tags if tags is empty")
                        if i[5] == "":
                            i[5] = "\"" + i[3] + "\""
                            debug_print(bugging, 1, "   tags is now: %s" % i[5])

                        array_to_save.append(i)
                    line += 1

    debug_print(bugging, 1, "saving touched up contents in a final .csv")

    with open("touched_up_and_combined.csv", "w", encoding="utf8") as output:
        output_writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        debug_print(bugging, 1, " writing header row")
        output_writer.writerow(
            ["Handle", "Title", "Body (HTML)", "Vendor", "Type", "Tags", "Published", "Option1 Name", "Option1 Value",
             "Option2 Name", "Option2 Value", "Option3 Name", "Option3 Value", "Variant SKU", "Variant Grams",
             "Variant Inventory Tracker", "Variant Inventory Qty", "Variant Inventory Policy",
             "Variant Fulfillment Service", "Variant Price", "Variant Compare At Price", "Variant Requires Shipping",
             "Variant Taxable", "Variant Barcode", "Image Src", "Image Position", "Image Alt Text", "Gift Card",
             "SEO Title", "SEO Description", "Google Shopping / Google Product Category", "Google Shopping / Gender",
             "Google Shopping / Age Group", "Google Shopping / MPN", "Google Shopping / AdWords Grouping",
             "Google Shopping / AdWords Labels", "Google Shopping / Condition", "Google Shopping / Custom Product",
             "Google Shopping / Custom Label 0", "Google Shopping / Custom Label 1", "Google Shopping / Custom Label 2",
             "Google Shopping / Custom Label 3", "Google Shopping / Custom Label 4", "Variant Image",
             "Variant Weight Unit", "Variant Tax Code", "Cost per item"])
        for i in array_to_save:
            debug_print(bugging, 1, " writing row for %s" % i[1])
            output_writer.writerow(i)




if __name__ == "__main__":
    touch_up_csvs(1)