<?php

    $valorSalario = 9;
    $valorSalario = ($valorSalario++);
    $valorSalario = $valorSalario /= 2;

    switch ($valorSalario){
        case 0:
            $valor = "Valor zero";
            break;
        case 5:
            $valor = "valor cinco";
            break;
        case 10:
            $valor = "valor dez";
            break;
        default:
            $valor = "valor menor que dez";            
    }
    echo $valor;
?>