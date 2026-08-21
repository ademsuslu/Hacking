# cut command


+ `-f1` **öncesini kesme**
+ `-f2` **sonrasını kesme**

## example payload


```cat tum_arsiv_linkleri.txt | grep "winId"                 
https://matlab.mathworks.com/matlab/23.2.0.2436196/window.html?winId=11d7f882-05a4-436e-8815-68eaf7478c19
https://matlab.mathworks.com/matlab/23.2.0.2436196/window.html?winId=1625729c-e429-4dff-8e98-dfee73b1a38c
https://matlab.mathworks.com/matlab/23.2.0.2436196/window.html?winId=1b490d61-9907-4730-b758-56ad7d259340
https://matlab.mathworks.com/matlab/23.2.0.2436196/window.html?winId=246aff36-401a-417d-99c9-c8f3260e5de7
https://matlab.mathworks.com/matlab/23.2.0.2436196/window.html?winId=2c225794-a254-479d-9e72-87634bd70797
https://matlab.mathworks.com/matlab/23.2.0.2436196/window.html?winId=5c76346a-f96c-4df5-90b2-2ec1ac00b450
https://matlab.mathworks.com/matlab/23.2.0.2436196/window.html?winId=7517f083-b6d2-4dca-9edc-3658980b247e
```


**`=`'den öncesini alma **


```bash
cut -d'=' -f1
```


```
cat tum_arsiv_linkleri.txt | grep "winId" |  cut -d'=' -f1

#output
https://matlab.mathworks.com/matlab/23.2.0.2436196/window.html?winId
https://matlab.mathworks.com/matlab/23.2.0.2436196/window.html?winId
https://matlab.mathworks.com/matlab/23.2.0.2436196/window.html?winId
https://matlab.mathworks.com/matlab/23.2.0.2436196/window.html?winId
```

**`=`'den sonrasını alma **


```bash
cut -d'=' -f2
```


```
cat tum_arsiv_linkleri.txt | grep "winId" | cut -d'=' -f2

#output
11d7f882-05a4-436e-8815-68eaf7478c19
1625729c-e429-4dff-8e98-dfee73b1a38c
1b490d61-9907-4730-b758-56ad7d259340
246aff36-401a-417d-99c9-c8f3260e5de7
2c225794-a254-479d-9e72-87634bd70797
5c76346a-f96c-4df5-90b2-2ec1ac00b450
```

