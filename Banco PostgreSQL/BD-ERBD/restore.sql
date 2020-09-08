--
-- NOTE:
--
-- File paths need to be edited. Search for $$PATH$$ and
-- replace it with the path to the directory containing
-- the extracted data files.
--
--
-- PostgreSQL database dump
--

-- Dumped from database version 12.4 (Ubuntu 12.4-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.4 (Ubuntu 12.4-0ubuntu0.20.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE erbd_atual;
--
-- Name: erbd_atual; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE erbd_atual WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'pt_BR.UTF-8' LC_CTYPE = 'pt_BR.UTF-8';


ALTER DATABASE erbd_atual OWNER TO postgres;

\connect erbd_atual

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: afiliacao; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.afiliacao (
    id integer NOT NULL,
    id_instituicao integer NOT NULL,
    id_autor integer NOT NULL,
    ano_inicio integer NOT NULL,
    ano_fim integer,
    funcao character varying(50)
);


ALTER TABLE public.afiliacao OWNER TO postgres;

--
-- Name: afiliacao_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.afiliacao_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.afiliacao_id_seq OWNER TO postgres;

--
-- Name: afiliacao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.afiliacao_id_seq OWNED BY public.afiliacao.id;


--
-- Name: artigos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.artigos_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.artigos_id_seq OWNER TO postgres;

--
-- Name: artigos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.artigos (
    id integer DEFAULT nextval('public.artigos_id_seq'::regclass) NOT NULL,
    titulo character varying(400) NOT NULL,
    tipo_id integer,
    edicao_id integer,
    fonte character varying(15),
    resumo character varying(1000)
);


ALTER TABLE public.artigos OWNER TO postgres;

--
-- Name: autores_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.autores_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.autores_id_seq OWNER TO postgres;

--
-- Name: autores; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.autores (
    id integer DEFAULT nextval('public.autores_id_seq'::regclass) NOT NULL,
    nome character varying(150) NOT NULL,
    genero character varying(75),
    artigossbbd integer,
    id_lattes bigint,
    nome_citado character varying(500),
    ultima_atualizacao date
);


ALTER TABLE public.autores OWNER TO postgres;

--
-- Name: autoresartigo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.autoresartigo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.autoresartigo_id_seq OWNER TO postgres;

--
-- Name: autoresartigo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.autoresartigo (
    id integer DEFAULT nextval('public.autoresartigo_id_seq'::regclass) NOT NULL,
    autor_id integer NOT NULL,
    artigo_id integer NOT NULL,
    ordem integer
);


ALTER TABLE public.autoresartigo OWNER TO postgres;

--
-- Name: edicoes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.edicoes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.edicoes_id_seq OWNER TO postgres;

--
-- Name: edicoes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.edicoes (
    id integer DEFAULT nextval('public.edicoes_id_seq'::regclass) NOT NULL,
    cidade character varying(40),
    uf character(2),
    data_inicio date,
    data_fim date,
    local character varying(15),
    tema character varying(100),
    veiculo character varying(400),
    id_tipo_veiculo integer,
    ano integer NOT NULL
);


ALTER TABLE public.edicoes OWNER TO postgres;

--
-- Name: formacao; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.formacao (
    id integer NOT NULL,
    id_titulacao integer NOT NULL,
    id_autor integer NOT NULL,
    ano_inicio integer NOT NULL,
    ano_fim integer,
    id_instituicao integer NOT NULL,
    curso character varying(1000)
);


ALTER TABLE public.formacao OWNER TO postgres;

--
-- Name: formacao_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.formacao_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.formacao_id_seq OWNER TO postgres;

--
-- Name: formacao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.formacao_id_seq OWNED BY public.formacao.id;


--
-- Name: instituicoes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.instituicoes (
    id integer NOT NULL,
    nome character varying(500) NOT NULL,
    uf character varying(20),
    cidade character varying(50)
);


ALTER TABLE public.instituicoes OWNER TO postgres;

--
-- Name: instituicoes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.instituicoes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.instituicoes_id_seq OWNER TO postgres;

--
-- Name: instituicoes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.instituicoes_id_seq OWNED BY public.instituicoes.id;


--
-- Name: tipos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tipos_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.tipos_id_seq OWNER TO postgres;

--
-- Name: tipos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tipos (
    id integer DEFAULT nextval('public.tipos_id_seq'::regclass) NOT NULL,
    nome character varying(50) NOT NULL
);


ALTER TABLE public.tipos OWNER TO postgres;

--
-- Name: tipoveiculo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tipoveiculo (
    id integer NOT NULL,
    nome character varying(30)
);


ALTER TABLE public.tipoveiculo OWNER TO postgres;

--
-- Name: tipoveiculo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tipoveiculo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tipoveiculo_id_seq OWNER TO postgres;

--
-- Name: tipoveiculo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tipoveiculo_id_seq OWNED BY public.tipoveiculo.id;


--
-- Name: titulacoes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.titulacoes (
    id integer NOT NULL,
    nome character varying(20)
);


ALTER TABLE public.titulacoes OWNER TO postgres;

--
-- Name: titulacoes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.titulacoes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.titulacoes_id_seq OWNER TO postgres;

--
-- Name: titulacoes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.titulacoes_id_seq OWNED BY public.titulacoes.id;


--
-- Name: afiliacao id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.afiliacao ALTER COLUMN id SET DEFAULT nextval('public.afiliacao_id_seq'::regclass);


--
-- Name: formacao id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formacao ALTER COLUMN id SET DEFAULT nextval('public.formacao_id_seq'::regclass);


--
-- Name: instituicoes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.instituicoes ALTER COLUMN id SET DEFAULT nextval('public.instituicoes_id_seq'::regclass);


--
-- Name: tipoveiculo id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipoveiculo ALTER COLUMN id SET DEFAULT nextval('public.tipoveiculo_id_seq'::regclass);


--
-- Name: titulacoes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.titulacoes ALTER COLUMN id SET DEFAULT nextval('public.titulacoes_id_seq'::regclass);


--
-- Data for Name: afiliacao; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.afiliacao (id, id_instituicao, id_autor, ano_inicio, ano_fim, funcao) FROM stdin;
\.
COPY public.afiliacao (id, id_instituicao, id_autor, ano_inicio, ano_fim, funcao) FROM '$$PATH$$/3065.dat';

--
-- Data for Name: artigos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.artigos (id, titulo, tipo_id, edicao_id, fonte, resumo) FROM stdin;
\.
COPY public.artigos (id, titulo, tipo_id, edicao_id, fonte, resumo) FROM '$$PATH$$/3068.dat';

--
-- Data for Name: autores; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.autores (id, nome, genero, artigossbbd, id_lattes, nome_citado, ultima_atualizacao) FROM stdin;
\.
COPY public.autores (id, nome, genero, artigossbbd, id_lattes, nome_citado, ultima_atualizacao) FROM '$$PATH$$/3070.dat';

--
-- Data for Name: autoresartigo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.autoresartigo (id, autor_id, artigo_id, ordem) FROM stdin;
\.
COPY public.autoresartigo (id, autor_id, artigo_id, ordem) FROM '$$PATH$$/3072.dat';

--
-- Data for Name: edicoes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.edicoes (id, cidade, uf, data_inicio, data_fim, local, tema, veiculo, id_tipo_veiculo, ano) FROM stdin;
\.
COPY public.edicoes (id, cidade, uf, data_inicio, data_fim, local, tema, veiculo, id_tipo_veiculo, ano) FROM '$$PATH$$/3074.dat';

--
-- Data for Name: formacao; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.formacao (id, id_titulacao, id_autor, ano_inicio, ano_fim, id_instituicao, curso) FROM stdin;
\.
COPY public.formacao (id, id_titulacao, id_autor, ano_inicio, ano_fim, id_instituicao, curso) FROM '$$PATH$$/3075.dat';

--
-- Data for Name: instituicoes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.instituicoes (id, nome, uf, cidade) FROM stdin;
\.
COPY public.instituicoes (id, nome, uf, cidade) FROM '$$PATH$$/3077.dat';

--
-- Data for Name: tipos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tipos (id, nome) FROM stdin;
\.
COPY public.tipos (id, nome) FROM '$$PATH$$/3080.dat';

--
-- Data for Name: tipoveiculo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tipoveiculo (id, nome) FROM stdin;
\.
COPY public.tipoveiculo (id, nome) FROM '$$PATH$$/3081.dat';

--
-- Data for Name: titulacoes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.titulacoes (id, nome) FROM stdin;
\.
COPY public.titulacoes (id, nome) FROM '$$PATH$$/3083.dat';

--
-- Name: afiliacao_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.afiliacao_id_seq', 483, true);


--
-- Name: artigos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.artigos_id_seq', 3984, true);


--
-- Name: autores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.autores_id_seq', 447, true);


--
-- Name: autoresartigo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.autoresartigo_id_seq', 4412, true);


--
-- Name: edicoes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.edicoes_id_seq', 3754, true);


--
-- Name: formacao_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.formacao_id_seq', 985, true);


--
-- Name: instituicoes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.instituicoes_id_seq', 167, true);


--
-- Name: tipos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tipos_id_seq', 4, true);


--
-- Name: tipoveiculo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tipoveiculo_id_seq', 3, true);


--
-- Name: titulacoes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.titulacoes_id_seq', 4, true);


--
-- Name: afiliacao afiliacao_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.afiliacao
    ADD CONSTRAINT afiliacao_pkey PRIMARY KEY (id);


--
-- Name: artigos artigos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artigos
    ADD CONSTRAINT artigos_pkey PRIMARY KEY (id);


--
-- Name: autores autores_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.autores
    ADD CONSTRAINT autores_pkey PRIMARY KEY (id);


--
-- Name: autoresartigo autoresartigo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.autoresartigo
    ADD CONSTRAINT autoresartigo_pkey PRIMARY KEY (id);


--
-- Name: edicoes edicoes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.edicoes
    ADD CONSTRAINT edicoes_pkey PRIMARY KEY (id);


--
-- Name: formacao formacao_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formacao
    ADD CONSTRAINT formacao_pkey PRIMARY KEY (id);


--
-- Name: instituicoes instituicoes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.instituicoes
    ADD CONSTRAINT instituicoes_pkey PRIMARY KEY (id);


--
-- Name: tipos tipos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipos
    ADD CONSTRAINT tipos_pkey PRIMARY KEY (id);


--
-- Name: tipoveiculo tipoveiculo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipoveiculo
    ADD CONSTRAINT tipoveiculo_pkey PRIMARY KEY (id);


--
-- Name: titulacoes titulacoes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.titulacoes
    ADD CONSTRAINT titulacoes_pkey PRIMARY KEY (id);


--
-- Name: fki_ixartigo; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fki_ixartigo ON public.autoresartigo USING btree (artigo_id);


--
-- Name: fki_ixautor; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fki_ixautor ON public.formacao USING btree (id_autor);


--
-- Name: fki_ixautoria; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fki_ixautoria ON public.autoresartigo USING btree (autor_id);


--
-- Name: fki_ixedicao; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fki_ixedicao ON public.artigos USING btree (edicao_id);


--
-- Name: fki_ixtipo; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fki_ixtipo ON public.artigos USING btree (tipo_id);


--
-- Name: fki_ixtipoveiculo; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fki_ixtipoveiculo ON public.edicoes USING btree (id_tipo_veiculo);


--
-- Name: afiliacao afiliacao_id_autor_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.afiliacao
    ADD CONSTRAINT afiliacao_id_autor_fkey FOREIGN KEY (id_autor) REFERENCES public.autores(id);


--
-- Name: afiliacao afiliacao_id_instituicao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.afiliacao
    ADD CONSTRAINT afiliacao_id_instituicao_fkey FOREIGN KEY (id_instituicao) REFERENCES public.instituicoes(id);


--
-- Name: formacao formacao_id_instituicao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formacao
    ADD CONSTRAINT formacao_id_instituicao_fkey FOREIGN KEY (id_instituicao) REFERENCES public.instituicoes(id);


--
-- Name: formacao formacao_id_titulacao_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formacao
    ADD CONSTRAINT formacao_id_titulacao_fkey FOREIGN KEY (id_titulacao) REFERENCES public.titulacoes(id);


--
-- Name: autoresartigo ixartigo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.autoresartigo
    ADD CONSTRAINT ixartigo FOREIGN KEY (artigo_id) REFERENCES public.artigos(id);


--
-- Name: formacao ixautor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.formacao
    ADD CONSTRAINT ixautor FOREIGN KEY (id_autor) REFERENCES public.autores(id);


--
-- Name: autoresartigo ixautor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.autoresartigo
    ADD CONSTRAINT ixautor FOREIGN KEY (autor_id) REFERENCES public.autores(id);


--
-- Name: artigos ixedicao; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artigos
    ADD CONSTRAINT ixedicao FOREIGN KEY (edicao_id) REFERENCES public.edicoes(id);


--
-- Name: artigos ixtipo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.artigos
    ADD CONSTRAINT ixtipo FOREIGN KEY (tipo_id) REFERENCES public.tipos(id);


--
-- Name: edicoes ixtipoveiculo; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.edicoes
    ADD CONSTRAINT ixtipoveiculo FOREIGN KEY (id_tipo_veiculo) REFERENCES public.tipoveiculo(id);


--
-- PostgreSQL database dump complete
--

