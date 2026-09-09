from crystalbuilder.bilbao import download_all_spacegroup_data 

def download_bilbao_data():
    print("This tool helps you connect to the Bilbao Crystallographic Server (BCS) and download local copies of the necessary generators for all space groups. K-vector fetching is currently not working.")
    print("The BCS uses Cloudflare protection to prevent large-scale web scraping. One way to still download the data is by passing this check in your browser and copying the cookie data to this tool")
    print("Begin by navigating to https://cryst.ehu.es/index.html and passing the CloudFlare check. Then right click and choose your browser's 'inspect' option. In 'storage' or similar locations, you should be able to see your cookies. Find 'turnstile_passed' and copy the 'value' of this cookie (it should be a string of numbers)")
    turnstile_string = input("Paste the turnstile_passed cookie value below or press ctrl+c to exit \n")
    while turnstile_string is not None:
        try:
            float(turnstile_string)
            break
        except:
            turnstile_string = input("Paste the turnstile_passed cookie value below or press ctrl+c to exit \n")
    force_redownload_opt = input("Redownload all data? Warning: This takes several minutes! (y/[n]) \n")
    boolcheck = force_redownload_opt.strip().lower() == str('y')
    print(boolcheck)
    if boolcheck:
        force_redownload = True
        print("forcing")
    else:
        force_redownload = False
    print("Trying to download space group data")
    download_all_spacegroup_data(cookie=turnstile_string, force_redownload=force_redownload)
    
if __name__ == "__main__":
    download_bilbao_data()