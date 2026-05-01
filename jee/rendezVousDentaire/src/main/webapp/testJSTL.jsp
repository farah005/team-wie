<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Test JSTL</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 40px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            max-width: 600px;
            margin: 0 auto;
        }
        h1 { color: #2196F3; }
        .success { color: #4CAF50; font-weight: bold; }
        .error { color: #f44336; font-weight: bold; }
        ul { list-style: none; padding: 0; }
        li { 
            padding: 10px; 
            margin: 5px 0; 
            background: #f8f9fa; 
            border-left: 4px solid #2196F3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 Test JSTL</h1>
        
        <!-- Test 1: Variable -->
        <h2>Test 1 : Variables</h2>
        <c:set var="message" value="JSTL fonctionne correctement !" />
        <p class="success">✅ ${message}</p>
        
        <!-- Test 2: Boucle -->
        <h2>Test 2 : Boucle (forEach)</h2>
        <ul>
            <c:forEach begin="1" end="5" var="i">
                <li>Item numéro ${i}</li>
            </c:forEach>
        </ul>
        
        <!-- Test 3: Condition -->
        <h2>Test 3 : Condition (if)</h2>
        <c:set var="nombre" value="10" />
        <p>La variable nombre vaut : ${nombre}</p>
        <c:if test="${nombre > 5}">
            <p class="success">✅ Le nombre est supérieur à 5</p>
        </c:if>
        
        <!-- Test 4: Choose (switch) -->
        <h2>Test 4 : Choose (switch)</h2>
        <c:set var="jour" value="3" />
        <c:choose>
            <c:when test="${jour == 1}">
                <p>Lundi</p>
            </c:when>
            <c:when test="${jour == 2}">
                <p>Mardi</p>
            </c:when>
            <c:when test="${jour == 3}">
                <p class="success">✅ Mercredi</p>
            </c:when>
            <c:otherwise>
                <p>Autre jour</p>
            </c:otherwise>
        </c:choose>
        
        <hr>
        <h2>🎉 Résultat</h2>
        <p class="success">
            Si vous voyez tous les tests ci-dessus avec les ✅, 
            alors JSTL est correctement installé !
        </p>
    </div>
</body>
</html>