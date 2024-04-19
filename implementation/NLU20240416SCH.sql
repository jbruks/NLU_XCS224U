--
-- PostgreSQL database dump
--

-- Dumped from database version 12.2
-- Dumped by pg_dump version 12.2

-- Started on 2024-04-19 11:13:45

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

--
-- TOC entry 8 (class 2615 OID 9532285)
-- Name: sch01; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA sch01;


ALTER SCHEMA sch01 OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 213 (class 1259 OID 9630787)
-- Name: answers; Type: TABLE; Schema: sch01; Owner: postgres
--

CREATE TABLE sch01.answers (
    pubmed_id character varying(50),
    simple_answer text,
    simple_answer_fsl text,
    complex_answer text,
    complex_answer_cot text
);


ALTER TABLE sch01.answers OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 9630777)
-- Name: questions; Type: TABLE; Schema: sch01; Owner: postgres
--

CREATE TABLE sch01.questions (
    pubmed_id character varying(50),
    simple_question text,
    complex_question text,
    complex_question_cot text
);


ALTER TABLE sch01.questions OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 9611955)
-- Name: t01; Type: TABLE; Schema: sch01; Owner: postgres
--

CREATE TABLE sch01.t01 (
    id integer NOT NULL,
    pubmed_id character varying(20),
    publication_date character varying(10),
    title text,
    abstract text,
    keywords text,
    journal text,
    conclusions text,
    methods text,
    results text,
    copyrights text,
    doi text,
    authors text,
    ac character varying(20),
    set_train_test character varying(10)
);


ALTER TABLE sch01.t01 OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 9630805)
-- Name: evaluation_view; Type: VIEW; Schema: sch01; Owner: postgres
--

CREATE VIEW sch01.evaluation_view AS
 SELECT t01.pubmed_id,
    t01.publication_date,
    t01.title,
    t01.abstract,
    t01.set_train_test,
    questions.simple_question,
    questions.complex_question,
    questions.complex_question_cot,
    answers.simple_answer,
    answers.simple_answer_fsl,
    answers.complex_answer,
    answers.complex_answer_cot
   FROM sch01.t01,
    sch01.questions,
    sch01.answers
  WHERE (((t01.pubmed_id)::text = (questions.pubmed_id)::text) AND ((t01.pubmed_id)::text = (answers.pubmed_id)::text) AND ((t01.set_train_test)::text = 'test'::text));


ALTER TABLE sch01.evaluation_view OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 9630850)
-- Name: evaluations; Type: TABLE; Schema: sch01; Owner: postgres
--

CREATE TABLE sch01.evaluations (
    pubmed_id character varying(50),
    sq_accuracy character varying(5),
    sq_relevance character varying(5),
    sq_compr character varying(5),
    sq_clarity character varying(5),
    sq_coherence character varying(5),
    sq_fsl_accuracy character varying(5),
    sq_fsl_relevance character varying(5),
    sq_fsl_compr character varying(5),
    sq_fsl_clarity character varying(5),
    sq_fsl_coherence character varying(5),
    cq_accuracy character varying(5),
    cq_relevance character varying(5),
    cq_compr character varying(5),
    cq_clarity character varying(5),
    cq_coherence character varying(5),
    cq_cot_accuracy character varying(5),
    cq_cot_relevance character varying(5),
    cq_cot_compr character varying(5),
    cq_cot_clarity character varying(5),
    cq_cot_coherence character varying(5)
);


ALTER TABLE sch01.evaluations OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 9593234)
-- Name: fsl_question_answer_examples; Type: TABLE; Schema: sch01; Owner: postgres
--

CREATE TABLE sch01.fsl_question_answer_examples (
    id integer NOT NULL,
    pubmed_id character varying(50),
    fsl_question text,
    fsl_answer text
);


ALTER TABLE sch01.fsl_question_answer_examples OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 9593232)
-- Name: fsl_results_id_seq; Type: SEQUENCE; Schema: sch01; Owner: postgres
--

CREATE SEQUENCE sch01.fsl_results_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sch01.fsl_results_id_seq OWNER TO postgres;

--
-- TOC entry 2881 (class 0 OID 0)
-- Dependencies: 205
-- Name: fsl_results_id_seq; Type: SEQUENCE OWNED BY; Schema: sch01; Owner: postgres
--

ALTER SEQUENCE sch01.fsl_results_id_seq OWNED BY sch01.fsl_question_answer_examples.id;


--
-- TOC entry 204 (class 1259 OID 9532300)
-- Name: messages; Type: TABLE; Schema: sch01; Owner: postgres
--

CREATE TABLE sch01.messages (
    id integer NOT NULL,
    sender character varying(255),
    receiver character varying(255),
    content text,
    "timestamp" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    read boolean DEFAULT false
);


ALTER TABLE sch01.messages OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 9532298)
-- Name: messages_id_seq; Type: SEQUENCE; Schema: sch01; Owner: postgres
--

CREATE SEQUENCE sch01.messages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sch01.messages_id_seq OWNER TO postgres;

--
-- TOC entry 2882 (class 0 OID 0)
-- Dependencies: 203
-- Name: messages_id_seq; Type: SEQUENCE OWNED BY; Schema: sch01; Owner: postgres
--

ALTER SEQUENCE sch01.messages_id_seq OWNED BY sch01.messages.id;


--
-- TOC entry 210 (class 1259 OID 9630690)
-- Name: questions_id_seq; Type: SEQUENCE; Schema: sch01; Owner: postgres
--

CREATE SEQUENCE sch01.questions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sch01.questions_id_seq OWNER TO postgres;

--
-- TOC entry 208 (class 1259 OID 9611953)
-- Name: t01_id_seq; Type: SEQUENCE; Schema: sch01; Owner: postgres
--

CREATE SEQUENCE sch01.t01_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sch01.t01_id_seq OWNER TO postgres;

--
-- TOC entry 2883 (class 0 OID 0)
-- Dependencies: 208
-- Name: t01_id_seq; Type: SEQUENCE OWNED BY; Schema: sch01; Owner: postgres
--

ALTER SEQUENCE sch01.t01_id_seq OWNED BY sch01.t01.id;


--
-- TOC entry 207 (class 1259 OID 9593252)
-- Name: t01_original; Type: TABLE; Schema: sch01; Owner: postgres
--

CREATE TABLE sch01.t01_original (
    pubmed_id character varying(20),
    publication_date character varying(10),
    title text,
    abstract text,
    keywords text,
    journal text,
    conclusions text,
    methods text,
    results text,
    copyrights text,
    doi text,
    authors text,
    ac character varying(20)
);


ALTER TABLE sch01.t01_original OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 9630783)
-- Name: v01; Type: VIEW; Schema: sch01; Owner: postgres
--

CREATE VIEW sch01.v01 AS
 SELECT t01.pubmed_id,
    t01.title,
    t01.abstract,
    questions.simple_question,
    questions.complex_question,
    questions.complex_question_cot,
    t01.set_train_test
   FROM sch01.t01,
    sch01.questions
  WHERE ((t01.pubmed_id)::text = (questions.pubmed_id)::text);


ALTER TABLE sch01.v01 OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 9630793)
-- Name: v02; Type: VIEW; Schema: sch01; Owner: postgres
--

CREATE VIEW sch01.v02 AS
 SELECT t01.pubmed_id,
    t01.title,
    t01.abstract,
    questions.simple_question,
    questions.complex_question,
    answers.simple_answer,
    answers.simple_answer_fsl,
    answers.complex_answer,
    answers.complex_answer_cot,
    t01.set_train_test
   FROM sch01.t01,
    sch01.questions,
    sch01.answers
  WHERE (((t01.pubmed_id)::text = (questions.pubmed_id)::text) AND ((t01.pubmed_id)::text = (answers.pubmed_id)::text));


ALTER TABLE sch01.v02 OWNER TO postgres;

--
-- TOC entry 2739 (class 2604 OID 9593237)
-- Name: fsl_question_answer_examples id; Type: DEFAULT; Schema: sch01; Owner: postgres
--

ALTER TABLE ONLY sch01.fsl_question_answer_examples ALTER COLUMN id SET DEFAULT nextval('sch01.fsl_results_id_seq'::regclass);


--
-- TOC entry 2736 (class 2604 OID 9532303)
-- Name: messages id; Type: DEFAULT; Schema: sch01; Owner: postgres
--

ALTER TABLE ONLY sch01.messages ALTER COLUMN id SET DEFAULT nextval('sch01.messages_id_seq'::regclass);


--
-- TOC entry 2740 (class 2604 OID 9611958)
-- Name: t01 id; Type: DEFAULT; Schema: sch01; Owner: postgres
--

ALTER TABLE ONLY sch01.t01 ALTER COLUMN id SET DEFAULT nextval('sch01.t01_id_seq'::regclass);


--
-- TOC entry 2744 (class 2606 OID 9593242)
-- Name: fsl_question_answer_examples fsl_results_pkey; Type: CONSTRAINT; Schema: sch01; Owner: postgres
--

ALTER TABLE ONLY sch01.fsl_question_answer_examples
    ADD CONSTRAINT fsl_results_pkey PRIMARY KEY (id);


--
-- TOC entry 2742 (class 2606 OID 9532309)
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: sch01; Owner: postgres
--

ALTER TABLE ONLY sch01.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id);


--
-- TOC entry 2746 (class 2606 OID 9611963)
-- Name: t01 t01_pkey; Type: CONSTRAINT; Schema: sch01; Owner: postgres
--

ALTER TABLE ONLY sch01.t01
    ADD CONSTRAINT t01_pkey PRIMARY KEY (id);


-- Completed on 2024-04-19 11:13:46

--
-- PostgreSQL database dump complete
--

