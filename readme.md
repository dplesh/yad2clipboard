# yad2clipboard

Transform yad2 post details into a brief textual format and copy it to the clipboard. convenient for:

* Link-less sharing of post details
* Calendar events description. e.g. visiting an apartment for rent

Currently supported post types:

* Housing (Buying houses, renting houses)
* Vehicles

## Usage

```
python yad2clipboard.py <post_url>
```

### Editing output format

To modify clipboard output format, edit the post type-specific template, e.g. for estate posts simply edit `estate_output_template.txt` using the keywords used in the default format:

```
{title}, {neighborhood} {city}
{price}
{rooms}חדרים , {floor} קומה , {area} מ"ר
{description}
{details_list}
{amenities_list}
{contactName} - {contact_number}
{url}
```

A template exists for each post type.



## Requirements

```
pyperclip
selenium
```

