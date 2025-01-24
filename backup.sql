--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: activity_sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.activity_sessions (
    id integer NOT NULL,
    app_id integer NOT NULL,
    start_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    end_time timestamp without time zone,
    is_tracking boolean DEFAULT true
);


ALTER TABLE public.activity_sessions OWNER TO postgres;

--
-- Name: activity_sessions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.activity_sessions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.activity_sessions_id_seq OWNER TO postgres;

--
-- Name: activity_sessions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.activity_sessions_id_seq OWNED BY public.activity_sessions.id;


--
-- Name: apps; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.apps (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    exe_path character varying(255),
    process_name character varying(255),
    alias character varying(255) NOT NULL
);


ALTER TABLE public.apps OWNER TO postgres;

--
-- Name: apps_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.apps_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.apps_id_seq OWNER TO postgres;

--
-- Name: apps_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.apps_id_seq OWNED BY public.apps.id;


--
-- Name: tracked_apps; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tracked_apps (
    id integer NOT NULL,
    app_id integer NOT NULL
);


ALTER TABLE public.tracked_apps OWNER TO postgres;

--
-- Name: tracked_apps_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tracked_apps_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tracked_apps_id_seq OWNER TO postgres;

--
-- Name: tracked_apps_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tracked_apps_id_seq OWNED BY public.tracked_apps.id;


--
-- Name: activity_sessions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activity_sessions ALTER COLUMN id SET DEFAULT nextval('public.activity_sessions_id_seq'::regclass);


--
-- Name: apps id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.apps ALTER COLUMN id SET DEFAULT nextval('public.apps_id_seq'::regclass);


--
-- Name: tracked_apps id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tracked_apps ALTER COLUMN id SET DEFAULT nextval('public.tracked_apps_id_seq'::regclass);


--
-- Data for Name: activity_sessions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.activity_sessions (id, app_id, start_time, end_time, is_tracking) FROM stdin;
\.


--
-- Data for Name: apps; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.apps (id, name, exe_path, process_name, alias) FROM stdin;
\.


--
-- Data for Name: tracked_apps; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tracked_apps (id, app_id) FROM stdin;
\.


--
-- Name: activity_sessions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.activity_sessions_id_seq', 1, false);


--
-- Name: apps_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.apps_id_seq', 1, false);


--
-- Name: tracked_apps_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tracked_apps_id_seq', 1, false);


--
-- Name: activity_sessions activity_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activity_sessions
    ADD CONSTRAINT activity_sessions_pkey PRIMARY KEY (id);


--
-- Name: apps apps_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.apps
    ADD CONSTRAINT apps_pkey PRIMARY KEY (id);


--
-- Name: tracked_apps tracked_apps_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tracked_apps
    ADD CONSTRAINT tracked_apps_pkey PRIMARY KEY (id);


--
-- Name: activity_sessions activity_sessions_app_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activity_sessions
    ADD CONSTRAINT activity_sessions_app_id_fkey FOREIGN KEY (app_id) REFERENCES public.apps(id);


--
-- Name: tracked_apps tracked_apps_app_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tracked_apps
    ADD CONSTRAINT tracked_apps_app_id_fkey FOREIGN KEY (app_id) REFERENCES public.apps(id);


--
-- PostgreSQL database dump complete
--

