# if an alerted item is no longer on the storefront, remove it from alerted list
# so the user can be re-notified when another of the same item is stocked
alerteditems = open("alerteditems.txt", "r+")
alerted = alerteditems.readlines()

alerteditemsnew = open("alerteditems.txt", "w+")
alertednew = alerteditems.readlines()

listing_gone = True
dummy = True

text = open("database.txt", "r")
listings = text.readlines()

for alert in alerted:
    for line in listings:
        if (alert.strip('\n').strip() == line.strip('\n').strip()):
            listing_gone = False

    if not listing_gone:
        alerteditemsnew.write(alert)

    listing_gone = True


text.close()
alerteditems.close()
alerteditemsnew.close()
