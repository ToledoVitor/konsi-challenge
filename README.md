# konsi-challenge


Se você está lendo esse readme ou o meu projeto te interessou, ou você irá 
avaliá-lo, então, seja bem vindo!

Esse projeto consiste em um "web crawler", capaz de acessar um site específico, 
no caso o site do extrato digital, e obter os benefícios de um dado cpf. Para 
isso, o crawler precisa ter a habilidade de fazer as requisições e de conseguir 
fazer login e se autenticar também.

Esse projeto é todo construído em python + [flask](https://flask.palletsprojects.com/en/2.2.x/),
sendo o flask o método que usarei para disponibilizar a API. O crawler 
disponibiliza uma API com dois endpoint's para retornar os dados.


## Rodando o projeto

Como já disse acima, o projeto é baseado em python, logo, seu primeiro passar é 
instalar o python (não vou dizer como instalar o python aqui, mas é bem simples)

O segundo passa é instalar as dependências que o projeto utiliza. Todas as 
depêndencias estão salvas em requirements.txt, com o python instalado, rode no 
terminal:
```bash
    pip install -r requirements.txt
```

Com tudo instalado, para rodar o projeto, basta usar o comando:
```bash
    python app
```

Isso já vai subir o Flask na porta 5000. Você já deve conseguir ver uma página 
de **Not found no navegador** nesse momento.

Obs: Você já deve ter feito isso, mas eu sugiro criar uma virtualenv antes de 
instalar os requisitos.


## Rodando com Docker (opcional)

Apesar de o Flask deixar tudo bem simples e a aplicação também ser bem simples, 
como a ideia aqui é mostrar conhecimento, decidi deixar também a opção de subir 
o projeto em Docker. Para isso, você precisará ter instalado o 
[docker](https://www.docker.com/) e o [docker compose](https://docs.docker.com/compose/)

Para checar sua instalação, você pode rodar no terminal
```bash
    docker version              # mostra versão do docker
    docker compose version      # mostra versão do docker
```

Tendo tudo instalado, basta você buildar as imagens:
```bash
    docker compose build
```

E depois subir os containers:
```bash
    docker compose up
```

Novamente, o docker já vai lidar com todas as dependências e requisitos do 
projeto e você já deve conseguir ver a página de **Not found no navegador**.

## Usando a API

Bom, uma vez que você já está rodando o projeto, seja pelo seu terminal seja 
pelo docker, você muito provavelmente vai querer testá-lo.

Existem dois endpoints criados que podem ser usados `/benefits/<cpf>` e 
`/benefits/<cpf>/simple`.

O primeiro endpoint vai retornar todos os dados obtidos na requisição, enquanto 
o segundo endpoint vai retornar apenas os benefícios em si.

Como no desafio foi pedido que se construisse um crawler que retornasse os 
beneficios do cpf, e não foi pedido os demais dados, não soube dizer se eles 
eram ou não importantes. Por conta disso, criei os dois endpoints que cobrem as 
duas alternativas.

Caso esse projeto tivesse um uso real, provavelmente iria validar qual seria a 
melhor solução com quem demandou a tarefa, mas como é apenas um teste, segui com 
as duas opções.

Como a aplicação desenvolvida é puramente uma API, não existindo nada visual 
(frontend) para acessarmos, é preciso que você saiba como fazer as requisições 
para conseguir testar a API. É claro que cada um tem seu jeito preferido, 
browser, shell, postman, etc. mas eu particularmente gosto de usar o Postman 
nesses casos. 


Se quiser testar direto pelo seu terminal, aqui são dois exemplos que você pode 
usar para testar os endpoints:
```bash
    curl --location 'http://127.0.0.1:5000/benefits/' \
    --form 'cpf="083.019.725-72"' \
    --form 'login_user="testekonsi"' \
    --form 'login_password="testekonsi"'
```

```bash
    curl --location 'http://127.0.0.1:5000/benefits/simple' \
    --form 'cpf="083.019.725-72"' \
    --form 'login_user="testekonsi"' \
    --form 'login_password="testekonsi"'
```

Ah, esse cpf que coloquei é válido e pode ser usado para consulta.


## Rodando os testes

Para esse projeto usei a estrutura de testes do [pytest](https://docs.pytest.org/en/7.2.x/) 
e todos os testes estão no arquivo `tests.py`.

Existem alguns testes que testam a função de validação do cpf, testam se o 
crawler define corretamente o usuário e senha de acesso, e se a resposta 
retornada do crawler é igual a esperada.

Para rodar os testes, no seu terminal rode o comando:
```bash
    pytest tests.py
```

Fique tranquilo pois todas as requisições estão mockadas nos testes, assim, ao 
rodá-los nenhuma requisição real será feita para o site verdadeiro.


## Como foi desenvolvido o projeto

Essa seção não tem um ar muito técnico, mas por se tratar de algo desenvolvido 
para um teste, achei legal compartilhar aqui um pouco sobre minha linha de 
raciocínio e como cheguei na solução final.

A minha lista de prioridades era:
1. Entender o fluxo comum
2. Entender as ações que importam
3. Entender como as requisições eram feitas
4. Entender o que as requisições retornavam
5. Entender o que as requisições pediam

Ou seja, quando recebi o email com as informações do teste, meu primeiro passo 
foi navegar no site como um usuário normal, e entender o que tinha que ser 
feito para que conseguisse chegar aos dados que queria.

Feito isso, precisei separar as ações importantes do fluxo das não importantes, 
como exemplo, **fechar o modal de avisos não era uma ação essencial,** 
**porém realizar o login já é uma ação essencial**.

Depois que entendi as ações, comecei a depurar as requests que o browser estava 
fazendo a cada momento, e assim consegui separar duas requisições principais que 
o chrome estava fazendo. **Login e busca do cpf**

Percebi que o login retornava no header da resposta um atributo chamado 
*Authorization* que é um bearer token usado para autenticar as demais requests. 
A busca do cpf só precisava desse token para autorizar e fazer a requisição.

Um problema encontrado no fluxo foi que o endpoint de login não aceitava a 
requisição e retornava um status code **forbidden 403**. Para resolver esse 
problema notei que no browser a requisição **definia a origin e o referer** no 
header, então bastou definir no código também para resolver o problema.


## Requests vs Selenium vs Scrapy vs ... 

Uma coisa legal de se falar aqui é que eu não usei nenhum framework de 
webscrapping como [Selenium](https://www.selenium.dev/) (talvez o mais famoso), 
ou [Scrapy](https://scrapy.org/).

Esses frameworks são realmente muito úteis e resolvem grandes problemas, mas por
serem feitos para grandes problemas também geram muita complexidade no projeto. 

Não existe a necessidade de baixar algo externo para um problema que é possível 
se resolver com requests mais simples. **Simple is better than complex.**

Esses frameworks são muito úteis quando é preciso navegar entre várias telas, 
interagir com vários elementos, como clicar em botões, menus e afins. 

No caso do desafio, era possível chegar aos benefícios apenas fazendo as 
requisições. Navegar através do site também resolveria o problema, mas só 
geraria mais complexidade desnecessária. Seria preciso fechar o modal inicial de
avisos, clicar no menu, escolher a opção, preencher o input, clicar no botão... 

Esse fluxo além de se tornar mais extenso se torna mais frágil, uma vez que 
provavelmente precisariamos navegar no site através das tags, classes e ids dos 
elementos, e por conta disso, caso elas mudem a aplicação tem que mudar também. 
Uma simples mudança no modal ou no input já seria capaz de quebrar a aplicação.

Entendendo o fluxo e fazendo apenas as requisições essenciais além de deixar 
o projeto menos complexo, também o deixamos mais resistente.


## Considerações finais

Este projeto foi desenvolvido como uma maneira de avaliação de aplicação para 
uma vaga. Assim, a ideia aqui é mostrar o máximo de conhecimento no mínimo de 
tempo.

Por conta disso, usei as linguagens e ferramentas que tenho maior domínio 
e deixei todo o fluxo o mais simple possível.

A aplicação desenvolvida resolve o problema proposto, mas com certeza existem 
muitas maneira possíveis de melhorar o que foi feito aqui. 

Creio que todo o código esteja bem limpo e legível e todo fluxo esteja bem 
auto-explicativo. Também tentei explicar bem nesse readme qual foi minha linha 
de pensamento e processo de resolução. Contudo, se houver algum dúvida do que 
foi feito aqui, o porque foi feito, ou como rodar a aplicação, sinta-se a 
vontade para entrar em contato comigo. 
