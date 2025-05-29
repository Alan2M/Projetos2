describe('acessar_home.cy.js', () => {
  it('deve acessar a página inicial e verificar conteúdo esperado', () => {
    cy.visit('/');
    cy.contains('Bem-vindo ao Solidreams!').should('exist'); // Conteúdo da página home do projeto
    cy.get('a[href="/login/"]').should('exist');
    cy.get('a[href="/cadastro/"]').should('exist');
  });
});