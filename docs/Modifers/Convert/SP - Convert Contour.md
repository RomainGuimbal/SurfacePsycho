It's purpose is to give several operation for conversions of trim contours. 

<img width="538" height="288" alt="image" src="https://github.com/user-attachments/assets/c80ab713-667d-4b39-a370-89646e4f8036" />

## Fit to UV
Since 0.9 version, the fit option for trim contour was removed (its usage could be confusing). The idea was that it scales any trim contour to fit the natural boundaries of the patch. Fit to UV provides a way to upgrade old patches using it as well as giving you access to the old behavior if you like.

## To Normalized Knot
Scales the trim contour of NURBS patch to fit in the range 0 to 1m while preserving the shape by scaling the knots too. This is very useful to edit an imported model. Some imported surfaces can commonly have contours ranging from 0 to 10km which make them impractical to edit.

## To NURBS
Convert contour segments of every type to NURBS

## To Rational Beziers
Convert contour segments of every type to Rational Beziers. This splits each span of NURBS.
