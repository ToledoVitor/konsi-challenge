# konsi-challenge

Se você está lendo esse readme ou o meu projeto te interessou, ou você irá 
avaliá-lo, então, seja bem vindo!

Esse projeto consiste em um "web crawler", capaz de acessar um site específico, 
no caso o site do extrato digital, e obter os benefícios de um dado cpf. Para 
isso, o crawler precisa ter a habilidade de fazer as requisições e de conseguir 
fazer login e se autenticar também.

Esse projeto é todo construído em python + [flask](https://flask.palletsprojects.com/en/2.2.x/),
sendo o flask o método que usarei para disponibilizar a API.

Ah, o crawler disponibiliza uma API com dois endpoint's, que retornaram os dados.


## Como rodar o projeto

Como já disse acima, o projeto é baseado em python, logo, seu primeiro passar é 
instalar o python (não vou dizer como instalar o python aqui, é simples, joga no 
google).

O segundo passa é instalar as dependências que o projeto utiliza. Todas as 
depêndencias estão salvas em requirements.txt, então tendo o python instalado, 
rode no terminal:
```bash
    pip install -r requirements.txt
```

Isso já irá ler todas as dependências listadas no arquivo e as intalará.

Com tudo instalado, para iniciar o projeto:
```bash
    python app
``` 

Obs: Você já deve saber bem disso, mas eu sugiro criar uma virtualenv antes de 
sair instalando os requisitos.


## Como foi desenvolvido o projeto

Essa seção não tem um ar muito técnico, mas por se tratar de algo desenvolvido 
para um teste técnico, acho legal compartilhar aqui um pouco sobre minha linha 
de raciocínio e como cheguei na solução final.

A minha lista de prioridades era:
1. Entender o fluxo comum
2. Entender as ações que importam
3. Entender como as requisições eram feitas
4. Entender o que as requisições retornavam
5. Entender o que as requisições pediam

Ou seja, quando recebi o email com as informações do teste, meu primeiro passo 
foi navegar no site como um usuário normal, e entender o que tinha que ser 
feito para que conseguisse chegar aonde queria.

Depois disso, precisava separar as ações importantes do fluxo, das não 
importantes, como exemplo, fechar o modal de avisos não era uma ação essencial, 
porém realizar o login já é uma ação essencial.

Depois que entendi as ações, comecei a depurar as requests que o browser estava 
fazendo a cada momento, assim, consegui separar duas requisições principais que 
o chrome estava fazendo. **Login e busca do cpf**

Percebi que o login retornava no header da resposta um atributo chamado 
*Authorization* que é um bearer token usado para autenticar as demais requests, 
e que a busca do cpf só precisava desse bearer token para fazer a requisição.

Um problema que encontrei no fluxo, era que o endpoint de login não aceitava a 
requisição e retornava um status code forbidden 403. Para resolver esse problema 
notei que no browser a requisição definia a origin e o referer no header, então 
bastou definir no código que resolvemos o problema.


## Requests vs Selenium vs Scrapy vs ... 

Uma coisa legal de se falar aqui é que, eu não usei nenhum framework de 
webscrapping como [Selenium](https://www.selenium.dev/) (talvez o mais famoso) 
ou [Scrapy](https://scrapy.org/).

Esses frameworks são realmente muito úteis e resolvem problemas bem grandes, mas 
também são grandes e geram muita complexidade no projeto. 

Não existe a necessidade de baixar algo externo para um problema que é possível 
se resolver com requests mais simples.

Esses frameworks também são muito úteis quando é preciso navegar entre várias 
telas e é necessário interagir com elas, como clicar em botões, menus ou afins. 

No caso do desafio, era possível chegar aos benefícios navegando através do site, 
mas isso novamente só geraria mais complexidade no código. Seria preciso fechar 
o modal inicial de avisos, clicar no menu, escolher a opção, preencher o input, 
clicar no botão... 

Esse fluxo além de se tornar complexo se torna mais sensível, uma vez que 
navegariamos pelo site usando as classes e tags dos elementos, e caso elas mudem 
a aplicação tem que mudar também. Uma mudança na classe do modal inicial, ou 
ainda, a remoção do modal já seria capaz de quebrar toda a aplicação.

Entendo o fluxo e fazendo apenas as requisições essenciais deixamos o projeto 
menos complexo, além de deixar mais resistente também.


## TODO: docker it
