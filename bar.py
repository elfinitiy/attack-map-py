import shared
import matplotlib.pyplot as plt
import re
re_payload = re.compile('.* - - \[.*\] "(.*?) HTTP/1\..".*')

#print(shared.bad_request_list)

payload_requests = shared.extract_re(shared.filtered_requests, re_payload, 1)
#print(payload_requests)
#quit()
dict_with_count = {}
for bad_request in payload_requests:
    if bad_request not in dict_with_count:
        dict_with_count[bad_request] = {"request": bad_request, "count": 0}
    dict_with_count[bad_request]["count"] += 1

sorted_list = sorted(dict_with_count.values(), key=lambda x: x["count"], reverse=True)
top_ten = sorted_list[:10]

print(top_ten)

labels = list(map(lambda x: x["request"][:32], top_ten))
data = list(map(lambda x: x["count"], top_ten))

index_list = list(range(0, len(labels)))
plt.bar(index_list, data)
plt.xlabel('Request payload', fontsize=8)
plt.ylabel('Request amount', fontsize=8)
plt.xticks(index_list, labels, fontsize=8, rotation=30)
plt.title('Most popular bad requests')
plt.show()
