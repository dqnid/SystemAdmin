#!/usr/bin/perl

use CGI;
use File::Slurper 'read_text';

my $q = CGI->new;

system("/bin/bash /etc/Scripts/servicios.sh");

my $apache = read_text('/var/www/html/servicios/apache2');
my $sshd = read_text('/var/www/html/servicios/sshd');
my $postfix = read_text('/var/www/html/servicios/postfix');
my $mariadb = read_text('/var/www/html/servicios/mariadb');

my @servicios = ($apache, $sshd,$postfix, $mariadb);
my @nombresServicios = ("Web", "SSH","Correo", "MariaDB");
my $i;

print $q->header;

print qq(
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="styles.css">
    <title>TrueSight</title>
</head>
<style>
body, html{
	width: 100%;
	background-color: #415a77;
	margin-left: 0px;
	margin-top: 0px;
}

.topnav-centered{
	position: relative;
	overflow: hidden;
	top: 0;
	text-align: center;
	background-color: #1b263b;	
	margin-top: 0px;
	width: 100%;
	margin-bottom: 20px;
	display: grid;    
	grid-template-columns: 1fr 1fr;
	grid-template-rows: 1fr;
	grid-auto-rows: minmax(100px, auto);
	gap: 20px;
}

.topnav-centered h1 {
	background-color: #1b263b;	
	color:white;
	height: 100%;
	vertical-align: middle;
	font-size: 60px;
	grid-column: 2;
	text-align: left;
}

.topnav-centered img{
	vertical-align: middle;
	text-align: center;
	width: 180px;
	grid-column: 1;
 	float: none;
  position: absolute;
  top: 50%;
  left: 40%;
  transform: translate(-50%, -50%);
}

.formulario{
	color: white;
	margin-left: 42%;
	margin-right: 42%;
	margin-top: 10%;
	font-size: 20px;
}

input{
	font-size: 20px;
	margin-top: 5px;
}

button{
	margin-top: 5px;
	font-size: 20px;
}

.navbar {
  background-color: #1b263b;
  overflow: hidden;
  position: fixed;
  bottom: 0;
  width: 100%;
  margin-left: 0px;
}

.navbar a {
  float: left;
  display: block;
  color: #f2f2f2;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
  font-size: 17px;
}

.navbar a:hover {
  background-color: #ddd;
  color: black;
}

.navbar a.active {
  background-color: #415a77;
  color: white;
}

.enlaces{
	margin-left: 40%;
}

.errorRegistro{
	margin-top: 15%;
	text-align: center;	
}

.errorRegistro p{
	font-size: 40px;	
	color: white;
}

.errorRegistro a{
	padding: 10px 10px 10px 10px;
	font-size: 30px;
	background-color: #1b263b;
	color: white;
}

.errorRegistro a:hover{
	background-color: #ddd;
	color: black;
}

.servicio_activo{
	font-size: 25px;
    background-color: #80ed99;
    padding: 5px;
    border-radius: 4px;
    margin-top: 10px;
    vertical-align: middle;
}

.servicio_inactivo{
	font-size: 25px;
    background-color: #e63946;
    color:#fff;
    padding: 5px;
    border-radius: 4px;
    margin-top: 10px;
    vertical-align: middle;
}

.servicios{
    margin-left: 40%;
    margin-right: 40%;
    text-align: center !important;
    vertical-align: middle;
    margin-top: 12%;
}

.elemento{
    height: 70px;
    width: 100%;
    margin-top: auto;
    vertical-align: middle;
}
</style>
<body>
	<div class="topnav-centered">
		<img src="./logo.png"/>
		<h1>TrueSight</h1>
	</div>
	
	<div class="navbar">
		<div class="enlaces">
	   		<a href="/index.html">Inicio</a>
	   		<a href="/inicio.html">Login</a>
	   		<a href="/registro.html">Registro</a>
	   		<a class="active">Recursos</a>
		</div>
	</div>
        <div class="servicios">
        );

        for ($i = 0; $i < @servicios; $i++){
          my $servicio = $nombresServicios[$i];
          if($servicios[$i] != 1){
            print qq(
              <div class="elemento">
                <label class="servicio_inactivo">$servicio: Inactivo</label>
              </div>);
          }else{
            print qq(
              <div class="elemento">
                <label class="servicio_activo">$servicio: Activo</label>
              </div>);
          }
        }
print qq(
        </div>
</body>
</html>);
