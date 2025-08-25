Crystalbuilder
===

crystalbuilder is a package that, as its name suggests, builds photonic crystals. This is really a frankenstein of existing software, including MPB, MEEP and Vedo. MPB is used for bandstructure simulations (and MEEP is used for MPB). Vedo is just a mesh viewer/editor that is used for displaying the generated crystals.

The package also uses beautifulsoup4 to read position data from the Bilbao Crystallographic Server, so that you can easily make structures corresponding to any of the 230 space groups. If you use this feature, make sure that the Bilbao server gets cited. The diamond cubic example shows how that should be done. 
