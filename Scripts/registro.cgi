#!/usr/bin/perl 
use strict;
use warnings;

use CGI;
use Linux::usermod;
use File::Path qw(make_path remove_tree);
use File::Copy;
use DBI;
use Email::Send::SMTP::Gmail;
use Time::Piece::MySQL;
use Quota;

my $q = CGI->new;

# Lectura de web
my $usr  = $q->param('usr');
my $passw = $q->param('passw');
my $esProfesor = $q->param('esProfesor');
my $correo = $q->param('email');
my $direccion = $q->param('dir');
my $nombre = $q->param('nombre');
my $mensaje = "Bienvenido a TrueSight, $nombre";
my $ape1 = $q->param('ape1');
my $ape2 = $q->param('segundo');
my $ruta;
my $codigo = int(rand( 9999-1001 ) ) + 1000;

my $grupo;
if($esProfesor){
	$grupo = '1003';
}else{
	$grupo = '1002';
}

my %usuarios = Linux::usermod->users();
for(keys %usuarios){
	if($_ eq $usr){
		print $q->redirect('/errorInicio.html');
		exit 0;
	}
}

my $directorio = make_path("/home/$usr");
$ruta = "/home/$usr"; 
Linux::usermod->add($usr,$passw,"",$grupo,$mensaje ,$ruta, "/bin/bash");
copy("/etc/condiciones.txt","$ruta/condiciones.txt") or die "Error al copiar las condiciones: $!";
# Crear carpeta Maildir

my $fecha = localtime;
$fecha = $fecha->mysql_datetime;

my $dbh = DBI->connect('DBI:MariaDB:database=sysadmin;host=localhost','admin','labii',{ RaiseError => 1, PrintError => 0 });

my $sth;
$sth = $dbh->prepare("insert into usuarios (nombre, usr, apellido1, apellido2, profesor, email, direccion, h_registro) values (?,?,?,?,?,?,?,?)") or die;
if($esProfesor){
    $sth->execute($nombre, $usr, $ape1, $ape2, 1, $correo, $direccion, $fecha) or die;
}else{
    $sth->execute($nombre, $usr, $ape1, $ape2, 0, $correo, $direccion, $fecha) or die;
}
$dbh->disconnect();
make_path("$directorio/public_html");
print $q->redirect('/exitoInicio.html');
