# Inspección de Código con SonarQube

## Primera inspección

### Issue 1
![Issue1](https://github.com/LaCalmaInc/GRP-Skibidi-Software-inc-2024-PROYINF/blob/main/inspections/issue1.png)

Los string duplicados hacen que el proceso de refactorizacion sea más complejo y propenso a errores, ya que cualquier cambio debe propagarse en todas las ocurrencias, esta duplicación como se menciono puede traer inconsistencias en el codigo y problemas dificiles de rastrear, SonarQube recomendo reemplazar los string duplicados por constantes para facilitar la gestión y reducir los errores al actualizar el código, se decidio implementar esta recomendación para mejorar la mantenibilidad el codigo.

Esta observacion de corrigio en el archivo "views.py".


### Issue 2
![Issue2](https://github.com/LaCalmaInc/GRP-Skibidi-Software-inc-2024-PROYINF/blob/main/inspections/issue2.png)

Se estaba cargando la secret key de Django en el repositorios, lo cual podria tener implicancias de seguridad graves, en caso de que el software entre en funcionamiento, como eludir la autenticación y acceder a datos sensibles de los usuarios. Es por esto que SonarQube recomendo, sacar la secret key del repositorio y usar un gestor para manejar estas, para garantizar la seguridad del código y proteger los futuros datos sensibles, se implemento el uso de la secret key con un archivo.txt, el cual estara guardado de forma local en el dispositivo.

Se utiliza el txt con la secret key y se agrego su ruta al .gitignore para no tener denuevo el mismo problema.

## Segunda inpección (Despues de corregir 2 Quality issues)
 


