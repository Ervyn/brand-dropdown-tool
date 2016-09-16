import json

#case sensitive comparison
def iequal(a, b):
	try:
		return a.upper() == b.upper()
	except AttributeError:
		return a == b

#read user input list
def read_user_input():
	content = []
	with open("brandInput.txt") as f:
		content = f.readlines()

	content = [x.strip('\n') for x in content]
	return content

#read BOB brands database dump
def load_brands():			
	input_file = read_user_input()[0] + "brandList.json"
	parsed_json = json.loads(open(input_file).read())
	return parsed_json

#read BOB brands database dump
def get_base_category_url():			
	return read_user_input()[1]

def get_failed_brands_list():
	failed_brands = [a for a in success_brands+read_user_input() if (a not in success_brands) or (a not in read_user_input())][2:]
	if(failed_brands):
		return "Couldn't find brands: " + str(failed_brands)
	else:
		return "Dropdown Code Generated Successfully"
	
success_brands = []
	
def main():	
	#base html str
	
	html_str = """
<ul class="mal">
	<a class="b-header__clickable" href='""" + get_base_category_url() + """?from=header'>
		<li class="b-header__category-dropdown-title">Top Brands</li>
	</a>

	<span class="b-header__hr"></span>
	"""

	parsed_json = load_brands()
	
	#loop over input brand list
	for y in read_user_input():
		x=0
				
		if 'https://www' in y:
			special_brand = y.split(' ')
			html_str += """
	<a class="b-header__clickable" href='""" + special_brand[1] + """?from=header'>"""	
			html_str += """
		<li class="pbm b-header__category-dropdown-item">""" + special_brand[0] + """</li>
	</a>
			"""
			success_brands.append(y) 
			x = x + 1
		else:	
			while x < len(parsed_json):
				if(iequal(y, parsed_json[x]['name'])):
					html_str += """
	<a class="b-header__clickable" href='""" + get_base_category_url() + parsed_json[x]['url_key'] + """/?from=header'>"""	
					html_str += """
		<li class="pbm b-header__category-dropdown-item">""" + parsed_json[x]['name'] + """</li>
	</a>
					"""
					success_brands.append(y)
					
				x = x + 1

	#html str end
	html_str += """
</ul>
	"""
		
	print get_failed_brands_list()
	
	Html_file= open("brandOutput.html","w")
	Html_file.write(html_str)
	Html_file.close()
	
if __name__ == "__main__":
	main()