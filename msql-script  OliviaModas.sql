create database OliviaModas;
use OliviaModas;

create table usuario(
	id int primary key auto_increment not null,
    nome varchar(100) not null,
    email varchar(100) not null, 
    senha varchar(20) not null,
    telefone varchar(20) not null, 
	categoria ENUM('ADM', 'Colaborador') NOT NULL,
    login VARCHAR(120) NOT NULL
);

-- Usando delimitador alternativo
DELIMITER $$

-- Criando o trigger
CREATE TRIGGER before_insert_usuarios
BEFORE INSERT ON usuario
FOR EACH ROW
BEGIN
    SET NEW.login = 
        CASE 
            WHEN NEW.categoria = 'ADM' THEN CONCAT('adm.', NEW.nome)
            WHEN NEW.categoria = 'Colaborador' THEN CONCAT('colab.', NEW.nome)
        END;
END $$

-- Restaurando o delimitador para ;
DELIMITER ;

INSERT INTO usuario (nome, email, senha, telefone, categoria)
VALUES ('Leonardo', 'leonardo@gmail.com', 'leo1234', '(11)000999111', 'ADM');

select * from usuario;
# DROP TRIGGER IF EXISTS before_insert_usuarios;

create table produtos(
	id int primary key auto_increment not null,
    nome varchar(100) not null,
    quantidade int not null, 
    tamanho varchar(10) not null,
    preco decimal(10,2) not null,
    descricao varchar(100),
    categoria ENUM('Camisa', 'Short', 'Calça', 'Tênis', 'Blusa')
);

ALTER TABLE produtos ADD COLUMN  genero ENUM('M', 'F') UNIQUE NOT NULL;
ALTER TABLE usuario change senha senha varchar(120);


INSERT INTO produtos (nome, quantidade, tamanho, preco, categoria, genero)
VALUES
('Camisa Polo Preta', '80', 'G', '84.00', 'Camisa', 'M'),
('Camisa Polo Branca', '80', 'G', '86.00', 'Camisa', 'M'),
('Camisa Regata Vermelha', '90', 'M', '55.00', 'Camisa', 'F'),
('Camisa Regata Amarela', '70', 'M', '50.00', 'Camisa', 'F'),
('Short Jeans Azul Escuro', '100', '42', '75.00', 'Short', 'M'),
('Short Jeans Azul Claro', '110', '38', '75.00', 'Short', 'F'),
('Calça Moletom', '120', '38', '60.00', 'Calça', 'F'),
('Calça Jeans Azul Claro', '120', '42', '98.00', 'Calça', 'M'),
('Calça Jeans Azul Escuro', '120', '38', '94.00', 'Calça', 'F'),
('Tenis Nike', '140', '40', '180.00', 'Tenis', 'M'),
('Tenis Addidas', '140', '36', '160.00', 'Tenis', 'F'),
('Blusa Branca', '80', 'M', '120.00', 'Blusa', 'F'),
('Blusa Preta', '80', 'G', '120.00', 'Blusa', 'M');

select * from produtos;
select * from usuario;
ALTER TABLE usuario MODIFY senha VARCHAR(256) NOT NULL;
