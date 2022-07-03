#!/usr/bin/perl

use strict;
use warnings;

use CGI;
use CGI::Session;
use Linux::usermod;
use Authen::PAM;
use POSIX qw(ttyname);
use DBI;

my $q = CGI->new;
my $pamh;
my $session;

my $username = $q->param('usr');
my $password = $q->param('passw');

sub my_conv_func {
    my @res;
    while ( @_ ) {
        my $code = shift;
        my $msg = shift;
 	my $ans = '';

 		$ans = $username if ($code == PAM_PROMPT_ECHO_ON());
		if ($code == PAM_PROMPT_ECHO_OFF()){
 			$ans = $password 
		}
 
       push @res, (PAM_SUCCESS(),$ans);
    }
    push @res, PAM_SUCCESS();
    return @res;
}

if (!ref($pamh = new Authen::PAM("passwd", $username, \&my_conv_func))) {
    print "Authen::PAM error de inicio\n";
    print $q->redirect('/errorBorrado.html');
    exit 1;
}

my $res = $pamh->pam_authenticate;

if($res == PAM_SUCCESS()){
	Linux::usermod->del($username);
	
	my $dbh = DBI->connect('DBI:MariaDB:database=sysadmin;host=localhost','admin','labii',{ RaiseError => 1, PrintError => 0 });
	my $sth;
	$sth = $dbh->prepare("delete from usuarios where usr=?") or die;
	$sth->execute($username) or die;
	$dbh->disconnect();

	print $q->redirect('/inicio.html');
}else{
	print $q->redirect('/errorBorrado.html');
}
