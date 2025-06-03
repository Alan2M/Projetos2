describe('Gestor - Login', () => {
  it('deve realizar login do gestor com sucesso', () => {
    cy.visit('/login');
    cy.get('input[name="email"]').type('gestor@email.com');
    cy.get('input[name="senha"]').type('123456');
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/gestor');
  });
});