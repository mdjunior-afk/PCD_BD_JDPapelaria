# Sistema de Gestão para Papelaria
___

**Desenvolvedores**

Márcio Douglas Cassemiro Junior, marcio.cassemiro@sga.pucminas.br

Luiz Felipe Assis Cavalcante, lfacavalcante@sga.pucminas.br

João Vitor de Lima, joao.lima.1594303@sga.pucminas.br

Gustavo Horta, gustavo.horta.1524459@sga.pucminas.br

Guilherme Amintas, email@sga.pucminas.br

Antônio Augusto, email@sga.pucminas.br
___

**Professor responsável**

Marco Paulo Soares Gomes
___
_Curso de Ciência de Dados, Unidade Praça da Liberdade_

_Instituto de Informática e Ciências Exatas – Pontifícia Universidade de Minas Gerais (PUC MINAS), Belo Horizonte – MG – Brasil_
___

## Resumo
 Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur vulputate a purus eu gravida. Suspendisse faucibus dictum venenatis. Donec bibendum vehicula condimentum. Ut facilisis velit ante. Vestibulum tellus urna, posuere ut interdum in, cursus eu lectus. Cras dictum augue ut ipsum pretium sodales. Aenean nec nisl non nunc tempor tincidunt. Duis ullamcorper turpis quis nulla feugiat, in lobortis dolor maximus. Morbi turpis est, malesuada porttitor mauris sed, pharetra ornare magna.

Vestibulum metus lectus, dignissim nec vehicula vel, imperdiet at augue. Duis et orci a tellus lobortis vehicula vel eu risus. Vestibulum eget erat id metus efficitur bibendum. Aliquam ullamcorper orci posuere nisi tristique, fermentum tincidunt nisl mollis. Sed a neque et erat luctus elementum. Praesent tempor ultrices vehicula. Quisque sit amet lorem elementum, sollicitudin lectus sit amet, sagittis lorem. Nullam blandit in purus eu venenatis.

## 1. Introdução
O projeto foi desenvolvido para atender às necessidades de uma papelaria localizada em Nova Lima/MG, uma empresa de pequeno porte que trabalha com aproximadamente 200 produtos. Seu portfólio é variado, abrangendo desde itens de informática, cadernos e canetas até serviços, como elaboração de currículos e produção de documentos para aluguel.

O principal desafio enfrentado pela empresa é a falta de controle eficiente do estoque e dos preços dos produtos. Para solucionar essa dificuldade, este projeto propõe a criação de um banco de dados que reúna todas as informações relevantes, aliado a um sistema desktop simplificado que auxilie na gestão dos produtos e serviços, trazendo maior organização e eficiência ao negócio.

## 2. Especificação do Minimundo

Essa seção apresenta a descrição textual do minimundo da Papelaria (v1.0), que tem como objetivo gerenciar os produtos, serviços, vendas, clientes e fornecedores da empresa. 

A papelaria comercializa diversos produtos, identificados por um código de barras e também por um código interno específico. Para cada produto devem ser armazenadas informações como: quantidade em estoque, preço de custo, preço de venda, estoque mínimo e, quando aplicável, a data de validade. O controle de reajustes de preço também deve ser registrado. A papelaria também mantém o cadastro de fornecedores, todos caracterizados como pessoas jurídicas. Para cada fornecedor devem ser salvos a razão social, CNPJ, endereço, telefone (um ou mais) e e-mail. Embora não estejam diretamente relacionados aos produtos, os dados dos fornecedores devem ser preservados para fins de controle administrativo.

Em relação às vendas, elas podem ser realizadas envolvendo tanto produtos quanto serviços, ou mesmo ambos na mesma transação. Cada venda deve armazenar a data em que ocorreu e as formas de pagamento utilizadas, sendo possível combinar mais de uma forma de pagamento na mesma venda (por exemplo, parte no cartão e parte em dinheiro). Uma venda pode estar vinculada a um cliente cadastrado ou ser realizada sem identificação do cliente. Os clientes da papelaria podem ser tanto pessoas físicas quanto jurídicas. Para pessoas físicas devem ser armazenados nome, CPF, data de nascimento, endereço, telefone e e-mail. Para pessoas jurídicas devem ser salvos razão social, CNPJ, endereço, telefone e e-mail. Além da comercialização de produtos, a papelaria também oferece serviços, como xerox, impressão de currículos, aluguel de equipamentos e fornecimento de diferentes tipos de papel. Cada serviço possui um tipo, podendo ter preços fixos ou variáveis, dependendo da natureza do serviço. A partir das informações de vendas (produtos e serviços), é possível apurar as receitas da papelaria. As despesas não são lançadas como entidade própria, mas sim calculadas em análises posteriores a partir das movimentações financeiras.

 ## 3. Projeto Conceitual
 
 <img width="1901" height="946" alt="Untitled Diagram drawio(2)" src="https://github.com/user-attachments/assets/fa21f967-a8b7-45af-86cc-d5ce48b24063" />

## 4. Projeto Lógico
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur vulputate a purus eu gravida. Suspendisse faucibus dictum venenatis. Donec bibendum vehicula condimentum. Ut facilisis velit ante. Vestibulum tellus urna, posuere ut interdum in, cursus eu lectus. Cras dictum augue ut ipsum pretium sodales. Aenean nec nisl non nunc tempor tincidunt. Duis ullamcorper turpis quis nulla feugiat, in lobortis dolor maximus. Morbi turpis est, malesuada porttitor mauris sed, pharetra ornare magna.

**Adicionar a imagem do diagrama**

## 5. Conclusão
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur vulputate a purus eu gravida. Suspendisse faucibus dictum venenatis. Donec bibendum vehicula condimentum. Ut facilisis velit ante. Vestibulum tellus urna, posuere ut interdum in, cursus eu lectus. Cras dictum augue ut ipsum pretium sodales. Aenean nec nisl non nunc tempor tincidunt. Duis ullamcorper turpis quis nulla feugiat, in lobortis dolor maximus. Morbi turpis est, malesuada porttitor mauris sed, pharetra ornare magna.
