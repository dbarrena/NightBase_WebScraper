promoters = [{}]

for promoter in promoters:
    if not promoter:
        promoters.remove(promoter)
if not promoters:
    promoters = None

print(promoters)