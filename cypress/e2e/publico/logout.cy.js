describe('logout.cy.js', () => {
  it('deve deslogar o usuário e redirecionar para a página de login', () => {
    
    cy.visit('/login/');
    cy.get('input[name="email"]').type('usuario_teste@email.com');
    cy.get('input[name="senha"]').type('senha123');
    cy.get('select[name="tipo"]').select('aluno');
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/'); 

    cy.visit('/logout/');

    cy.url().should('eq', 'http://127.0.0.1:8000/'); 

  });
});
