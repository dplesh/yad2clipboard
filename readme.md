# yad2clipboard

Scrape and transform yad2 post details into a brief textual format and copy it to the clipboard. convenient for:

* Link-less sharing of post details
* Calendar events description. e.g. visiting an apartment for rent

Currently supported post types:

* Housing (Buying houses, renting houses)
* Vehicles

## Usage

```
python yad2clipboard.py <post_url>
```

In case the site's captcha kicks in, the module will pop up the browser window for user interaction.

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
* Windows
* Python 3.9
* Python modules:

```
pyperclip
selenium
```
To run headless selenium, the module uses Gecko driver and Firefox binary (Chrome currently fails to run headless).

Make sure after you install the Gecko (Firefox) driver you add it's directory to system path (on windows). Default installation directory is `C:\Program Files (x86)\Mozilla\GeckoDriver`

As for the Firefox binary, the module expects it to be at the default installation directory of `C:\Program Files\Mozilla Firefox\firefox.exe`


