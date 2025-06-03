describe('Redirecionamento ao acessar sem login', () => {
  it('deve redirecionar para login ao acessar /formulario/ sem estar autenticado', () => {
    cy.visit('/formulario/');
    cy.url().should('include', '/login');
    cy.contains('Não tem uma conta? Registre-se').should('exist');
  });

  it('deve redirecionar para login ao acessar /gestor/ sem estar autenticado', () => {
    cy.visit('/gestor/');
    cy.url().should('include', '/login');
  });
});