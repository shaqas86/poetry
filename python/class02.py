marks:int=50
if marks >=50:
    print("pass")
else:
    print("fail")

fruits: dict[str]={"cherry", "banana","apple"}
print(fruits) 

fruits: dict[int,str]={1:"cherry",2: "banana",3:"apple"}
print(fruits[1])

# Start with users that need to be verified,
# and an empty list to hold confirmed users.users.py 
unconfirmed_users:list[str] = ['alice', 'brian', 'candace']
confirmed_users :list[str]= []
# Verify each user until there are no more unconfirmed users.
# Move each verified user into the list of confirmed users.
while unconfirmed_users:
    current_user = unconfirmed_users.pop()
 
print("Verifying user: " + current_user.title())
confirmed_users.append(current_user)
 
# Display all confirmed users.
print("\nThe following users have been confirmed:")
for confirmed_user in confirmed_users:
 print(confirmed_user.title())