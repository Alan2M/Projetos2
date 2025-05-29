describe('login_usuario.cy.js', () => {
  it('deve permitir login com credenciais válidas', () => {
    cy.visit('/login/');
    cy.get('input[name="email"]').type('usuario_teste@email.com');
    cy.get('input[name="senha"]').type('senha123');
    cy.get('select[name="tipo"]').select('aluno'); // ou 'professor' dependendo do teste
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/');
  });

  it('deve exibir erro com credenciais inválidas', () => {
    cy.visit('/login/');
    cy.get('input[name="email"]').type('invalido@email.com');
    cy.get('input[name="senha"]').type('senha_errada');
    cy.get('select[name="tipo"]').select('aluno'); // lembrar disso
    cy.get('button[type="submit"]').click();
    cy.contains('E-mail ou senha incorretos!').should('exist');
  });
});
