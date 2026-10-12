# Install and Setup

## Install
### Get it from the official [Extension platform↗️](https://extensions.blender.org/add-ons/surfacepsycho/) 

Or search for "Surface Psycho" directly in your Blender user preferences

## Setup

### Asset library

To register the library, in `Preferences > Add-ons > SurfacePsycho` and click `Add assets path`

<img src="https://github.com/RomainGuimbal/SurfacePsycho/assets/39882829/0a982227-9129-4100-bc03-849f52b707a5" width="400">

You should find a new Asset library in your asset browser

<img src="https://github.com/RomainGuimbal/SurfacePsycho/assets/39882829/fd346539-6ec8-403c-8f0a-2c7d1f72c0d8" width="400">

> This simply adds a path to `Preferences > File Paths > Asset Libraries`

## Matcaps
To register SP matcaps go to `Preferences > Add-ons > SurfacePsycho > Psycho Matcaps` and click `Add`

<img width="500" height="auto" alt="image" src="https://github.com/user-attachments/assets/7aa3f052-84b3-48b5-b448-688b7e213e9e" />

## Troubleshoot
If you encounter any issue not described below, please [report it ↗️](https://github.com/RomainGuimbal/SurfacePsycho/issues).
### "DLL not found"
In some still unclear configurations, the add-on fails to load with an error "DLL not found". To fix it go to your extension folder
`...\Blender Foundation\Blender\X.X\extensions` and delete `.cache` and `.local` folders. This will force to reinstall the external python modules.
> If you encounter any issue with this procedure, please let me know.