from office365.sharepoint.client_context import ClientContext

siteUrl = "https://test.sharepoint.com/sites/GamePoint-DEV"
clientID = ""
tenantUrl = ".onmicrosoft.com"
thumbprint = ""
certPath = ""
try:
    ctx = ClientContext(siteUrl).with_client_certificate(
        tenant=tenantUrl,
        client_id=clientID,
        cert_path=certPath,
        thumbprint=thumbprint
    )

    list = ctx.web.lists.get_by_title("BT News").get().execute_query()
    print(f"Total Items : {list.item_count}")
    items = ctx.web.lists.get_by_title("BT News").items.get_all(5000).execute_query()
    for item in items:
        print(f"ID -  {item.properties.get('ID')} | Title -  {item.properties.get('Title')} | News Summary - {item.properties.get('NewsSummary')}")
    #ctx.load(list)
    #ctx.execute_query()

    
except Exception as e:
    print(e)
    print("Error during exceution")
