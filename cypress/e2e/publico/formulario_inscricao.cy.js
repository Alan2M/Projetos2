describe('Validação do Formulário Solidreams', () => {
  beforeEach(() => {
    // Acessa a página de login
    cy.visit('/login/')

    // Preenche os dados de login
    cy.get('input[name="email"]').type('novo@email.com')
    cy.get('input[name="senha"]').type('senha123')
    cy.get('select[name="tipo"]').select('aluno')

    // Clica no botão de login
    cy.get('button[type="submit"]').click()

    // Espera o redirecionamento após login
    cy.url().should('not.include', '/login')

    // Agora acessa a página do formulário
    cy.visit('/formulario/')
  })

  it('Deve bloquear envio sem preencher campos obrigatórios', () => {
    cy.get('button[type="submit"]').click()
    cy.focused().should('have.attr', 'name', 'pessoas_moram')
  })

  it('Deve bloquear envio se selects obrigatórios não forem selecionados', () => {
    cy.get('input[name="pessoas_moram"][value="Moro sozinho"]').check({ force: true })
    cy.get('input[name="casa"][value="Própria"]').check({ force: true })
    cy.get('input[name="localizacao"][value="Zona urbana"]').check({ force: true })
    cy.get('input[name="trabalha"][value="Sim"]').check({ force: true })

    cy.get('button[type="submit"]').click()
    cy.focused().should('have.attr', 'name', 'escolaridade_pai')
  })
})
