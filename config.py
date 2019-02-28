config = {
    "url" : "https://vml1wk054.cse.ust.hk",
    "normal_port": 43333,
    "xss_port": 43334,
    "sql_port": 43335,
    #===============temp===============
    "dos_port": 43333,
    "error_port": 43333,
    "tampering_port": 43333,
    "xxe_port": 43333,
    "file_upload_port": 43333,
    "site_visiting_port": 43333,
    #==================================
    "set_up_mode": False,
    "verbose": False,
    "user_David": "David",
    "user_Petra": "Petra",
    "user_Albert": "Albert",
    "sleep_min": 5,
    "sleep_max": 15,
    "return_home_probability": 0.05,
    "comment_product_probability": 0.4 ,
    "home_product_clicks_max": 3,
    "home_product_clicks_min": 1,
    "add_product_to_cart_max": 10,
    "add_product_to_cart_min": 1,
    "add_product_to_cart_prob": 1
}

#add more comment when you are free
good_comments = ['Impressive','WOW','amazing!','One of my favorites!','I like this!','Thanks', 'amazing!', 'Interesting!', 'the products are good!!','Thank you','admin is nice','Not bad.','Good','Nice','I like this website','Great','splendid']

bad_comments = ['pathetic','horrible','ARE YOU KIDDING ME?','Soooooooooooo bad','I hate this', 'Garbage!','POOR SERVICE!!!!!','The ui is ugly','this is bad']

search_keyword = ['hoodie','hoodie', 'apple','apple','apple','juice','juice', 'Juice', 'owasp','orange', 'pizza', 'happiness']

ssh_config = {
    "hostname":"vml1wk054.cse.ust.hk",
    "username":"root",
    "key_filename":"C:\\Users\\david\\Desktop\\cse_vm_key\\prikey", 
    "passphrase":"<key passphrase>"
}