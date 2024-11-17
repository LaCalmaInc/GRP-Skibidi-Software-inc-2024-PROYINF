# Inspección de Código con SonarQube

![WhatsApp Image 2024-11-16 at 2 11 20 PM](https://github.com/user-attachments/assets/9efc7ad5-71bf-4fca-8f15-9b12f6d060f0)


## Primera inspección

### Issue 1
![Issue1](https://github.com/LaCalmaInc/GRP-Skibidi-Software-inc-2024-PROYINF/blob/main/inspections/issue1.png)

Los string duplicados hacen que el proceso de refactorizacion sea más complejo y propenso a errores, ya que cualquier cambio debe propagarse en todas las ocurrencias, esta duplicación como se menciono puede traer inconsistencias en el codigo y problemas dificiles de rastrear, SonarQube recomendo reemplazar los string duplicados por constantes para facilitar la gestión y reducir los errores al actualizar el código, se decidio implementar esta recomendación para mejorar la mantenibilidad el codigo.

Esta observacion de corrigio en el archivo "views.py".


### Issue 2
![Issue2](https://github.com/LaCalmaInc/GRP-Skibidi-Software-inc-2024-PROYINF/blob/main/inspections/issue2.png)

Se estaba cargando la secret key de Django en el repositorios, lo cual podria tener implicancias de seguridad graves, en caso de que el software entre en funcionamiento, como eludir la autenticación y acceder a datos sensibles de los usuarios. Es por esto que SonarQube recomendo, sacar la secret key del repositorio y usar un gestor para manejar estas, para garantizar la seguridad del código y proteger los futuros datos sensibles, se implemento el uso de la secret key con un archivo.txt, el cual estara guardado de forma local en el dispositivo.

Se utiliza el txt con la secret key y se agrego su ruta al .gitignore para no tener denuevo el mismo problema. Para la entrega se mantendrá este archivo txt visible en el repositorio para la revision del hito, pero que conste que es solo para efectos de la revision y no deberia ser asi.

## Segunda inspección (Despues de corregir 2 Quality issues)

Los issues que fueron corregidos, fueron solucionados exitosamente, no reportandoce en la la nueva inspección, disminuyendo los issues totales del software de 39 a 37.

![Grafico](https://github.com/LaCalmaInc/GRP-Skibidi-Software-inc-2024-PROYINF/blob/main/inspections/image.webp)
 


