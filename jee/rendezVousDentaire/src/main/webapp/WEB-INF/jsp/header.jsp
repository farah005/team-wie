<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/functions" prefix="fn" %>

<nav style="background: #4A3F35; color: white; padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
    <div style="font-size: 1.2rem; font-weight: bold; letter-spacing: 1px;">
        🦷 CABINET SOURIRE
    </div>
    
    <div style="display: flex; align-items: center; gap: 20px;">
        <c:if test="${not empty sessionScope.idConnecte}">
            <span style="font-size: 0.9rem; opacity: 0.9;">
                Connecté en tant que : <strong>${sessionScope.email}</strong> 
                <span style="background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; margin-left: 5px; text-transform: uppercase;">
                    ${sessionScope.userType}
                </span>
            </span>
            
            <div style="display: flex; gap: 15px; border-left: 1px solid rgba(255,255,255,0.3); padding-left: 15px;">
                <a href="${pageContext.request.contextPath}/rendezvous" style="color: white; text-decoration: none; font-size: 0.9rem;">Mes RDV</a>
                <c:if test="${fn:toLowerCase(sessionScope.userType) == 'aide-soignant' || fn:toLowerCase(sessionScope.userType) == 'dentiste'}">
                    <a href="${pageContext.request.contextPath}/service?action=list" style="color: white; text-decoration: none; font-size: 0.9rem;">Services</a>
                    <a href="${pageContext.request.contextPath}/actemedical?action=list" style="color: white; text-decoration: none; font-size: 0.9rem;">Actes médicaux</a>
                </c:if>
                <a href="${pageContext.request.contextPath}/deconnexion" 
                   style="color: #FF7675; text-decoration: none; font-weight: bold; font-size: 0.9rem; border: 1px solid #FF7675; padding: 3px 10px; border-radius: 5px;">
                   Déconnexion
                </a>
            </div>
        </c:if>
        
        <c:if test="${empty sessionScope.idConnecte}">
            <a href="${pageContext.request.contextPath}/connexion" style="color: white; text-decoration: none;">Connexion</a>
            <a href="${pageContext.request.contextPath}/patient" style="color: white; text-decoration: none; background: #6B5B4B; padding: 5px 12px; border-radius: 5px;">S'inscrire</a>
        </c:if>
    </div>
</nav>